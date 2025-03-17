import os
import json
from openai import OpenAI
import base64

# 定义函数用于编码图像
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# 初始化OpenAI客户端
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 读取train_26173.json文件
with open('/data1/user/md/workspace/NTIRE/yb_LLaMA-Factory/data/evalmuse/train_26173.json', 'r') as file:
    data = json.load(file)
samples = data

# 遍历每个样本
for i, sample in enumerate(samples):
    img_path = sample['img_path']
    prompt = sample['prompt']
    total_score = sample['total_score']
    element_score = sample['element_score']
    elements = ', '.join(element_score.keys())
    prompt_result = {
    'total_score': sample['total_score'],
    'element_score': sample['element_score']}
    base64_image = encode_image("/data1/user/md/workspace/NTIRE/yb_LLaMA-Factory/data/evalmuse/images/"+img_path)
    # 存储API调用的结果
    results = []
    try:
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
                        {"type": "text", "text": f"For this image, the text prompt is [{prompt}], and the key element is [{elements}]. Suppose the alignment scores for the total alignment score and each element alignment score are as follows: {prompt_result}. The score range for total_score is (0-5), and the score range for each element is (0-1). Please provide me with the thought process behind these scores, let's think step by step."},
                    ],
                },
            ],
        )
        results.append(completion.choices[0].message.content)
        # 保存结果到JSON文件
        output_dir = "/data1/user/md/workspace/NTIRE/yb_LLaMA-Factory/my_cot_data"
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{img_path}.json".replace("/", "_"))

        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
        print(f"Saved results for sample {i+815} to {output_file}")
    except Exception as e:
        print(f"Error: {e}")
        continue  # 继续下一个迭代
    
    