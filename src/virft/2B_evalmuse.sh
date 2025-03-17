export DATA_PATH=/root/autodl-tmp/data/evalmuse_6k
export CKPT_PATH=/root/Qwen2-VL-2B-Instruct
export SAVE_PATH=/root/autodl-tmp/Qwen2-VL-2B-Instruct_EvalMuse_New

export DEBUG_MODE="true" # Enable Debug if you want to see the rollout of model during RL
export LOG_PATH="./debug_log_2b_GRPO_evalmuse_6k.txt"

torchrun --nproc_per_node="2" \
    --nnodes="1" \
    --node_rank="0" \
    --master_addr="127.0.0.1" \
    --master_port="12345" \
    /root/Visual-RFT/src/virft/src/open_r1/grpo_match.py \
    --output_dir ${SAVE_PATH}  \
    --model_name_or_path ${CKPT_PATH} \
    --dataset_name ${DATA_PATH} \
    --deepspeed ./local_scripts/zero3.json \
    --max_prompt_length 1024 \
    --per_device_train_batch_size 1 \
    --gradient_accumulation_steps 2 \
    --logging_steps 1 \
    --bf16 \
    --report_to wandb \
    --gradient_checkpointing false \
    --attn_implementation flash_attention_2 \
    --max_pixels 401408 \
    --num_train_epochs 2 \
    --run_name EvalMuse_New \
    --save_steps 1000 \
    --save_only_model true \
    --num_generations 7
