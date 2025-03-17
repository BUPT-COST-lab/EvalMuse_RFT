import json

# Read data from the input JSON file
with open('/data1/user/md/workspace/NTIRE/yb_LLaMA-Factory/data/evalmuse/test_6544.json', 'r', encoding='utf-8') as infile:
    data = json.load(infile)

# Processing the data
output_data = []
for entry in data:
    element_score_str = ', '.join([f"{key}: {value}" for key, value in entry["element_score"].items()])
    elements = ', '.join(entry['element_score'].keys())
    processed_entry = {
        "instruction": "Begin by considering whether the overall concept of the prompt is captured in the image. Then, analyze the specific elements listed, focusing on the presence of key objects, their attributes, and relationships. Finally, perform two scoring tasks based on your analysis: overall score (0-5) and element scoring (0-1 per element).",
        "input": f"For this image<image>, the text prompt is [{entry['prompt']}], and the element list is [{elements}]",
        "output": f"total_score: {entry['total_score']}, element_score: {{{element_score_str}}}",
        "images": [f"/data1/user/md/workspace/NTIRE/yb_LLaMA-Factory/data/evalmuse/images/{entry['img_path']}"]
    }
    output_data.append(processed_entry)

# Write the processed data to a new JSON file
with open('/data1/user/md/workspace/NTIRE/yb_LLaMA-Factory/data/evalmuse_test_data_md_3.json', 'w', encoding='utf-8') as outfile:
    json.dump(output_data, outfile, ensure_ascii=False, indent=2)

print("Processing complete. Data written to 'processed_data.json'.")