#!/bin/bash
# 请根据实际情况修改以下目录路径：
expected_dir="/data1_8t/user/yb/LLaMA-Factory/results"  # 第一个目录：用来判断文件是否缺失
source_dir="/data1_8t/user/yb/LLaMA-Factory/data"      # 第二个目录：包含同名文件
target_dir="/data1_8t/user/yb/LLaMA-Factory/data/evalmuse_test_50"      # 第三个目录：目标目录，将文件移动到这里

# 记录缺失文件名的文件（可选）
missing_list="missing_files.txt"
> "$missing_list"  # 清空或创建文件

for i in {1..120}; do
    filename="evalmuse_test_${i}.json"
    if [ ! -f "$expected_dir/$filename" ]; then
        echo "$filename is missing" | tee -a "$missing_list"
        # 在另一个目录中查找同名文件，如果存在则移动到目标目录
        if [ -f "$source_dir/$filename" ]; then
            mv "$source_dir/$filename" "$target_dir/"
            echo "Moved $filename from source to target"
        else
            echo "$filename not found in source directory."
        fi
    fi
done

echo "Done. Missing files recorded in $missing_list."
