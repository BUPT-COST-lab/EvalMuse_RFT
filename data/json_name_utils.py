import json

result = {}
for i in range(1, 198):
    key = f"evalmuse_test_2/evalmuse_test_{i}"
    result[key] = {
        "file_name": f"{key}.json",
        "columns": {
            "prompt": "instruction",
            "query": "input",
            "response": "output",
            "images": "images"
        }
    }
with open('/data1/user/md/workspace/NTIRE/yb_LLaMA-Factory/scripts/data/result_2.json','w', encoding='utf-8')as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
