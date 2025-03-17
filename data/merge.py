import os
import json

def merge_json_files(input_dir, output_file):
    """
    遍历 input_dir 目录下所有 .json 文件，
    将它们的内容合并为一个大的 JSON 数组，
    并写入 output_file 文件中。
    """
    merged_data = []
    
    # 遍历目录下的所有 JSON 文件
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(input_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 如果 JSON 文件内部是列表，则将其扩展到 merged_data，
                    # 否则将整个对象追加到 merged_data 中。
                    if isinstance(data, list):
                        merged_data.extend(data)
                    else:
                        merged_data.append(data)
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {e}")

    # 确保输出目录存在
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as out_f:
        json.dump(merged_data, out_f, ensure_ascii=False, indent=2)
    print(f"合并完成，共合并 {len(merged_data)} 条数据，输出到 {output_file}")

if __name__ == '__main__':
    # 修改以下路径为你的实际目录和输出文件路径
    input_directory = '/data1/user/md/workspace/NTIRE/yb_LLaMA-Factory/results_3'   # 存放多个 JSON 文件的目录
    output_json = '/data1/user/md/workspace/NTIRE/yb_LLaMA-Factory/results_3/merged.json'  # 合并后生成的 JSON 文件路径

    merge_json_files(input_directory, output_json)