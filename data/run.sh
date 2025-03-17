# #!/bin/bash
# 提取数字并保存到一个数组中
# numbers=($(grep -oP '\d+' data_2.txt))

# 遍历数组中的每个数字
# for i in "${numbers[@]}"
for i in {1..197}
do
    echo "Running evalmuse_test_$i..."
    CUDA_VISIBLE_DEVICES=2,3 python /data1/user/md/workspace/NTIRE/yb_LLaMA-Factory/scripts/vllm_infer.py --model_name_or_path /data1/user/md/workspace/NTIRE/yb_LLaMA-Factory/outputs_3/qwen2_5_vl_lora_sft_md --dataset evalmuse_test_2/evalmuse_test_$i --template qwen2_vl
done

python /data1/user/md/workspace/NTIRE/yb_LLaMA-Factory/scripts/data/merge.py
python /data1/user/md/workspace/NTIRE/yb_LLaMA-Factory/scripts/data/result_utils.py

