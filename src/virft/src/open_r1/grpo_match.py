# Copyright 2025 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

from datasets import load_dataset, load_from_disk
from transformers import Qwen2VLForConditionalGeneration

from math_verify import parse, verify
# from open_r1.trainer import Qwen2VLGRPOTrainer
from trainer import Qwen2VLGRPOTrainer, Qwen2VLGRPOVLLMTrainer
from trl import GRPOConfig, GRPOTrainer, ModelConfig, ScriptArguments, TrlParser, get_peft_config

import json

# import wandb
# wandb.init(project="huggingface", id="qlj3m58f", resume="must")

@dataclass
class GRPOScriptArguments(ScriptArguments):
    """
    Script arguments for the GRPO training script.

    Args:
        reward_funcs (`list[str]`):
            List of reward functions. Possible values: 'accuracy', 'format'.
    """

    reward_funcs: list[str] = field(
        default_factory=lambda: ["accuracy", "format"],
        metadata={"help": "List of reward functions. Possible values: 'accuracy', 'format'"},
    )
    max_pixels: Optional[int] = field(
        default=12845056,
        metadata={"help": "Maximum number of pixels for the image"},
    )
    min_pixels: Optional[int] = field(
        default=3136,
        metadata={"help": "Minimum number of pixels for the image"},
    )


def extract_score(response):
    start_tag = "<answer>"
    end_tag = "</answer>"
    input_str = response
    # Check if the start tag is in the string
    if start_tag in input_str:
        # Extract the content between the start tag and end tag
        start_idx = input_str.find(start_tag) + len(start_tag)
        end_idx = input_str.find(end_tag)

        # If end_tag is not found (i.e., the string is truncated), assume it should be at the end
        if end_idx == -1:
            end_idx = len(input_str)

        content_str = input_str[start_idx:end_idx]
        
        # Check if it ends with a closing bracket, if not, fix it
        if not content_str.endswith("]"):
            # If the string is truncated, remove the incomplete part
            content_str = content_str.rsplit("},", 1)[0] + "}]"

        # Replace single quotes with double quotes for valid JSON
        content_str_corrected = content_str.replace("'", '"')

        # Convert the corrected string to a list of dictionaries (JSON format)
        try:
            score = json.loads(content_str_corrected)
        except json.JSONDecodeError as e:
            score = None
    else:
        score = None
    return score

def calculate_match(gt, predict):
    total_reward = abs(predict[0]['total_score'] - gt[0]['total_score'])
    score_results = []
    for element in predict[0]['element_score']:
        if element in gt[0]['element_score']:
            score_results.append(abs(predict[0]['element_score'][element] - gt[0]['element_score'][element]))
    score_results.extend([0] * (len(gt[0]['element_score']) - len(score_results)))
    score_results.append(total_reward / 5)
    # print(f"cauculate_match: {score_results}")
    return sum(score_results) / len(score_results)

def accuracy_reward_match(completions, solution, **kwargs):
    """Reward function that checks if the completion is correct using either symbolic verification or exact string matching."""
    contents = [completion[0]["content"] for completion in completions]


    rewards = []
    current_time = datetime.now().strftime("%d-%H-%M-%S-%f")
    for content, sol in zip(contents, solution):
        # print(f"content before: {content}")
        content = content.replace('\n', '')
        reward = 0.0
        # Try symbolic verification first
        try:
            answer = parse(content)
            if float(verify(answer, parse(sol))) > 0:
                reward = 1.0
                # print("all right")
        except Exception:
            pass  # Continue to next verification method if this fails
        
        student_answer_scores = []
        ground_truth_scores = []
        show_flage = 0

        # If symbolic verification failed, try string matching
        if reward == 0.0:
            try:
                show_flage = 1
                # Extract answer from solution if it has think/answer tags
                ground_truth = sol.strip()
                # print(f"ground_truth: {ground_truth}")
                # Extract answer from content if it has think/answer tags
                content_match = re.search(r'<answer>(.*?)</answer>', content)
                student_answer = content_match.group(1).strip() if content_match else content.strip()
                student_answer = '<answer>' + student_answer + '</answer>'
                # print(f"student_answer_before: {student_answer}")
                # fix format error
                student_answer = student_answer.replace("[[", '[')
                student_answer = student_answer.replace("]]", ']')
                student_answer = student_answer.replace("\n", '')
                student_answer = student_answer.replace("\r",'')
                student_answer = student_answer.replace("}]}]",'}}]')


                # print(f"student_answer_after: {student_answer}")
                # [{'Position': [254, 303, 291, 365], 'Confidence': 0.9}, {'Position': [100, 100, 200, 200], 'Confidence': 0.8}]
                ground_truth_scores = extract_score(ground_truth)
                # print(f"ground_truth_scores: {ground_truth_scores}")
                student_answer_scores = extract_score(student_answer)
                # print(f"student_answer_scores: {student_answer_scores}")
                # pdb.set_trace()
                if student_answer_scores == None or type(student_answer_scores[0]) != dict:  # wrong bbox
                    reward = 0.0
                else:
                    reward = calculate_match(ground_truth_scores, student_answer_scores)
                    if reward > 1:
                        reward = 1.0
                    if reward < 0:
                        reward = 0.0
            except Exception:
                pass  # Keep reward as 0.0 if both methods fail

        # print(f"accuracy_reward_match: {reward}")
        rewards.append(reward)
        # import pdb; pdb.set_trace()
        if os.getenv("DEBUG_MODE") == "true":
            log_path = os.getenv("LOG_PATH")
            # local_rank = int(os.getenv("LOCAL_RANK", 0))
            with open(log_path, "a") as f:
                f.write(f"------------- {current_time} Accuracy reward of scores: {reward} -------------\n")
                f.write(f"content: {content}\n")
                f.write(f"sol: {sol}\n")
                if show_flage == 1:
                    f.write(f"student_answer_bbox: {student_answer_scores}\n")
                    f.write(f"ground_truth_bbox: {ground_truth_scores}\n")
                    if student_answer_scores != None:
                        f.write(f"match_results: {reward}\n")
        show_flage = 0
    return rewards


def format_reward(completions, **kwargs):
    """Reward function that checks if the completion has a specific format. """
    pattern = r"<think>.*?</think>\s*<answer>.*?</answer>"
    # pattern = r"<answer>.*?</answer>"
    # print(f"origin completions: {completions}")
    completion_contents = [completion[0]["content"] for completion in completions]
    # matches = [re.match(pattern, content) for content in completion_contents]
    matches = [re.fullmatch(pattern, content, re.DOTALL) for content in completion_contents]
    return [1.0 if match else 0.0 for match in matches]


###  reward registry two parts
reward_funcs_registry = {
    "accuracy_match": accuracy_reward_match,
    "format": format_reward,
}

SYSTEM_PROMPT = (
    "A conversation between User and Assistant. The user asks a question, and the Assistant solves it. The assistant "
    "first thinks about the reasoning process in the mind and then provides the user with the answer. The reasoning "
    "process and answer are enclosed within <think> </think> and <answer> </answer> tags, respectively, i.e., "
    "<think> reasoning process here </think><answer> answer here </answer>"
)


def main(script_args, training_args, model_args):
    # Get reward functions
    script_args.reward_funcs = ['accuracy_match', 'format']
    reward_funcs = [reward_funcs_registry[func] for func in script_args.reward_funcs]

    # Load the dataset from huggingface
    # dataset = load_dataset(script_args.dataset_name, name=script_args.dataset_config)
    # Load the dataset from local disk
    from datasets import DatasetDict
    dataset = DatasetDict.load_from_disk(script_args.dataset_name)

    # Format into conversation
    def make_conversation(example):
        return {
            "prompt": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": example["problem"]},
            ],
        }

    def make_conversation_image(example):
        return {
            "prompt": [
                {
                    "role": "user",
                    "content": [
                        {"type": "image"},
                        {"type": "text", "text": example["problem"]},
                    ],
                },
            ],
        }

    if "image" in dataset[script_args.dataset_train_split].features:
        print("has image in dataset")
        dataset = dataset.map(make_conversation_image)  # Utilize multiprocessing for faster mapping
        # dataset = dataset.remove_columns(["original_question", "original_answer"])

    else:
        print("no image in dataset")
        dataset = dataset.map(make_conversation)
        dataset = dataset.remove_columns("messages")

    trainer_cls = Qwen2VLGRPOTrainer if not training_args.use_vllm else Qwen2VLGRPOVLLMTrainer
    print("using: ", trainer_cls)

    # Initialize the GRPO trainer
    trainer = trainer_cls(
        model=model_args.model_name_or_path,
        reward_funcs=reward_funcs,
        args=training_args,
        train_dataset=dataset[script_args.dataset_train_split],
        eval_dataset=dataset[script_args.dataset_test_split] if training_args.eval_strategy != "no" else None,
        peft_config=get_peft_config(model_args),
        attn_implementation=model_args.attn_implementation,
        max_pixels=script_args.max_pixels,
        min_pixels=script_args.min_pixels,
    )

    # Train and push the model to the Hub
    trainer.train()

    # Save and push to hub
    trainer.save_model(training_args.output_dir)
    if training_args.push_to_hub:
        trainer.push_to_hub(dataset_name=script_args.dataset_name)


if __name__ == "__main__":
    parser = TrlParser((GRPOScriptArguments, GRPOConfig, ModelConfig))
    script_args, training_args, model_args = parser.parse_args_and_config()
    main(script_args, training_args, model_args)
