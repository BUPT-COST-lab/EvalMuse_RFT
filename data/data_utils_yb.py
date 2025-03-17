import json


mode = "train"

# Read data from the input JSON file
with open(f'/data1/user/md/workspace/NTIRE/yb_LLaMA-Factory/data/evalmuse/train_26173.json', 'r', encoding='utf-8') as infile:
    data = json.load(infile)

# Processing the data
output_data = []
for idx, entry in enumerate(data):
    # keys = [key for key, _ in entry["element_score"].items()]
    # values = [value for _, value in entry["element_score"].items()]
    # input_template = "[{'total_score': s, 'element_score': {" + ', '.join([f"'{keys[i]}': s{i + 1}" for i in range(len(keys))]) + "}}]"
    # output_template = f"[{{'total_score': {entry['total_score']}, 'element_score': {{" + ', '.join([f"'{keys[i]}': {values[i]}" for i in range(len(keys))]) + "}}]"
    name 
    # 指定 JSON 文件路径
    json_file_path = '/data1/user/md/workspace/NTIRE/yb_LLaMA-Factory/my_cot_data/'+str(entry['img_path'])+'.json ' # 请根据实际情况修改文件路径

    # 读取 JSON 文件内容
    with open(json_file_path, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
        
    
    
#     processed_entry = {
#         "problem":
#             "Evaluate the input description according to the image. First, provide the total score to evaluate how well the image matches the full description (from 0 to 5, float). Second, provide element scores to evaluate how well the image matches the element words (from 0 to 1, float). "
#             "For element scores, evaluation is based on part-of-speech understanding. Action-related scores assess whether an object is performing the specified action, object-related scores determine its presence, and quantifier-related scores verify if the noun appears in the given quantity. Style-related scores evaluate adherence to a specified style, spatial relationship scores check positional accuracy, and adjective-related scores assess whether the modified noun aligns with the described attribute. And so on. "
#             "Output the thinking process in <think> </think> and final answer in <answer> </answer> tags. The output answer format should be as follows: "
#             f"<think> ... </think> <answer>{input_template}</answer> Please strictly follow the format.",
#         "solution": f"<answer>{output_template}</answer>",
#         "image_path": [f"/data1_8t/user/yb/LLaMA-Factory/data/evalmuse/images/{entry['img_path']}"]
#     }
#     output_data.append(processed_entry)

# # Write the processed data to a new JSON file
# with open(f'/data1_8t/user/yb/data_process/train_data.json', 'w', encoding='utf-8') as outfile:
#     json.dump(output_data, outfile, ensure_ascii=False, indent=2)

# print(f"Processing complete.")
