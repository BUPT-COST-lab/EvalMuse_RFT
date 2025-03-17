import os
from openai import OpenAI
import base64


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
base64_image = encode_image("/data1/user/md/workspace/NTIRE/yb_LLaMA-Factory/data/evalmuse/images/LCM-SDXL/01627.png")

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen2.5-vl-72b-instruct",
    messages=[
        {
            "role": "system",
            "content": [{"type": "text", "text": "You are an expert in evaluating alignment between the text prompt and the AI-generated image."}],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"}, 
                },
                {"type": "text", "text": "For this image, the text prompt is [sharing cheese is a serious felony, stop sign, do not do it. bad behavior. your family is ashamed. image from the bible], and the key element is ['sharing (activity)', 'cheese (food)', 'serious felony (attribute)', 'stop sign (object)', 'bad behavior (attribute)', 'family (human)', 'image from the bible (object)', 'do not do it (activity)', 'ashamed (attribute)']. Suppose the alignment scores for the total alignment score and each element alignment score are as follows: {'total_score': 2.666667, 'element_score': {'sharing (activity)': 0.666667, 'cheese (food)': 1.0, 'serious felony (attribute)': 0.0, 'stop sign (object)': 0.0, 'bad behavior (attribute)': 0.0, 'family (human)': 1.0, 'image from the bible (object)': 0.333333, 'do not do it (activity)': 0.0, 'ashamed (attribute)': 0.333333}}. The score range for total_score is (0-5), and the score range for each element is (0-1). Please provide me with the thought process behind these scores, let's think step by step."},
            ],
        },
    ],
)

print(completion.choices[0].message.content)