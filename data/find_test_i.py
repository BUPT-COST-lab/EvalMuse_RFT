import os
import json
import ast

no_find_json_list = []
# 读取txt文件中的路径列表
with open('data.txt', 'r') as f:
    content = f.read().strip()  # 去除可能的空白字符
txt_paths = ast.literal_eval(content)

# 存储匹配的JSON文件及其对应的路径
matches = {}

# JSON文件所在的文件夹路径（需要修改为你的实际路径）
json_folder = '/data1/user/md/workspace/NTIRE/yb_LLaMA-Factory/data/evalmuse_test_2'

# 遍历所有JSON文件
for json_filename in os.listdir(json_folder):
    if not json_filename.endswith('.json'):
        continue
    
    json_path = os.path.join(json_folder, json_filename)
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading {json_filename}: {e}")
        continue
    
    # 存储当前文件中找到的匹配路径
    found_paths = set()
    
    for entry in data:
        for image_path in entry.get('images', []):
            # 检查是否以任何txt路径结尾
            for tp in txt_paths:
                if image_path.endswith(tp):
                    found_paths.add(tp)
    
    # 如果有匹配路径则记录结果
    if found_paths:
        matches[json_filename] = list(found_paths)

# 打印结果
print("匹配结果:")
for filename, paths in matches.items():
    print(f"文件: {filename}")
    no_find_json_list.append(filename)
    print("包含路径:")
    for path in paths:
        print(f"  - {path}")
    print()

with open('data_2.txt', 'w') as f:
    f.write(str(no_find_json_list))  # 去除可能的空白字符