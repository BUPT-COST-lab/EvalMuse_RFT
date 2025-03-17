import os
import json

def filter_entries_by_png_existence(json_path, folder_path, output_json_path):
    # 读取 JSON 文件
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 用于存储需要保留的条目
    filtered_data = []
    
    # 遍历 JSON 中的每个条目
    for entry in data:
        # 获取 img_path 并去掉 .json 后缀
        img_path = entry.get("img_path", "")
        if not img_path:
            continue  # 如果 img_path 不存在，跳过
        
        # 检查对应的 PNG 文件是否存在
        png_file_path = os.path.join(folder_path, img_path)
        if not os.path.exists(png_file_path):
            # 如果 PNG 文件不存在，保留该条目
            filtered_data.append(entry)
    
    # 将过滤后的数据保存到新的 JSON 文件
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, indent=4)
    
    print(f"Filtered data saved to {output_json_path}")

# 替换为你的文件路径
json_path = '/data1/user/md/workspace/NTIRE/yb_LLaMA-Factory/data/evalmuse/train_mask.json'  # 输入的 JSON 文件路径
folder_path = '/data1/user/md/workspace/NTIRE/yb_LLaMA-Factory/my_cot_data'  # 存放 PNG 文件的文件夹路径
output_json_path = '/data1/user/md/workspace/NTIRE/yb_LLaMA-Factory/final_data/no_cot_train_mask.json'  # 输出的 JSON 文件路径

# 调用函数
filter_entries_by_png_existence(json_path, folder_path, output_json_path)