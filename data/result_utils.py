import json

count = 0
not_find_list = []
# 样例数据 A 和 B
with open('results_3/merged.json', 'r', encoding='utf-8') as infile:
    A = json.load(infile)

with open('data/evalmuse_test.json', 'r', encoding='utf-8') as infile:
    B = json.load(infile)


def update_B_with_A(A, B):
    global count
    # 以 A 中 images 的最后两级目录（例如 "SDXL-Turbo/00805.png"）作为 key 构建映射
    image_map = {
        item["images"][0].split("/")[-2] + "/" + item["images"][0].split("/")[-1]: item
        for item in A
    }

    for idx, b_item in enumerate(B):
        img_path = b_item["img_path"]

        if img_path in image_map:
            corresponding_A_item = image_map[img_path]
            # 从 output 字符串中提取 total_score
            output_str = corresponding_A_item["predict"]
            # 例如： "total_score: 0.53333, element_score: {...}"
            total_score_part = output_str.split(",")[0]  # "total_score: 0.53333"
            try:
                total_score = float(total_score_part.split(":")[1].strip())
            except Exception as e:
                print(f'bug: {idx}: {img_path}: {total_score_part}, Exception: {e}')
            # print("*"*70)
            # print(b_item)
            # print("*"*70)
            b_item["total_score"] = total_score
            # 解析 element_score 部分
            element_score_str = output_str.split("element_score: ")[1]
            try:
                element_score_str = element_score_str.rstrip("}").lstrip("{")
            except Exception as e:
                print(f'bug: {idx}: {img_path}: {element_score_str}, Exception: {e}')
            element_score_pairs = [pair.split(": ") for pair in element_score_str.split(", ")]
            try:
                element_score_A = {
                    pair[0]: None if pair[1] == "None" else float(pair[1])
                    for pair in element_score_pairs
                }
            except Exception as e:
                print(f'bug: {idx}: {img_path}: {element_score_pairs}, Exception: {e}')
            # 更新 B 中的 element_score，对于不存在的关键字默认赋值 0.5
            # b_item["element_score"] = {
            #     key: element_score_A.get(key, 0.5) for key in b_item["element_score"].keys()
            # }
            for key in b_item["element_score"].keys():
                if key in element_score_A:
                    b_item["element_score"][key] = element_score_A[key]  # 这里修正了对 b_item["element_score"] 的赋值方式
                else:
                    print(f'bug: {idx}: {img_path}: {key} not found')
                    # user_input = input("输入 1 赋值为 0.5，输入 0 退出程序: ").strip()
                    #
                    # if user_input == "1":
                    #     b_item["element_score"][key] = 0.5
                    # elif user_input == "0":
                    #     print("程序终止")
                    #     exit()  # 直接退出程序
                    # else:
                    #     print("无效输入，默认赋值 0.5")
                    #     b_item["element_score"][key] = 0.5  # 如果输入无效，默认赋值
        else:
            # 如果 A 中找不到对应的图片，则全部赋默认值 0.5
            b_item["element_score"] = {key: 0.5 for key in b_item["element_score"].keys()}
            b_item["total_score"] = 3
            print(f'not found: {img_path}')
            count+=1
            not_find_list.append(img_path)
        del b_item["prompt_id"]
        del b_item["type"]
        del b_item["promt_meaningless"]
        del b_item["split_confidence"]
        del b_item["attribute_confidence"]
        del b_item["fidelity_label"]

    return B


# 更新 B 数据
updated_B = update_B_with_A(A, B)

# 以 JSON 格式打印输出 B
with open('results_3/output.json', 'w', encoding='utf-8') as outfile:
    json.dump(updated_B, outfile, ensure_ascii=False, indent=4)

# 假设你的JSON数据存储在一个文件中
with open('results_3/output.json', 'r') as file:
    data = json.load(file)

# 遍历JSON数据
for item in data:
    element_score = item.get('element_score', {})
    for key in element_score:
        if element_score[key] is None:
            element_score[key] = 0.5

# 将修改后的数据写回文件（如果需要）
with open('results_3/output_1.json', 'w') as file:
    json.dump(data, file, indent=4)

print("修改完成！")
print("数据已保存到 output_1.json")
print(count)
with open("data.txt", "w") as text_file:
    text_file.write(str(not_find_list))