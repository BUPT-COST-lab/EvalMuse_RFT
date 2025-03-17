import json
import math

def split_json_file(input_file, output_prefix, part_size):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    total = len(data)
    n = math.ceil(total / part_size)

    for i in range(n):
        start = i * part_size
        end = start + part_size
        part = data[start:end]
        output_file = f"{output_prefix}_{i+1}.json"
        with open(output_file, "w", encoding="utf-8") as out:
            json.dump(part, out, ensure_ascii=False, indent=4)
        print(f"Saved part {i+1} to {output_file} with {len(part)} items.")

# 示例用法：将 input.json 分割成 3 份，并保存为 output_1.json, output_2.json, output_3.json
split_json_file("/data1/user/md/workspace/NTIRE/yb_LLaMA-Factory/data/evalmuse_test_data_md_2.json", "/data1/user/md/workspace/NTIRE/yb_LLaMA-Factory/data/evalmuse_test_2/evalmuse_test", 55)
