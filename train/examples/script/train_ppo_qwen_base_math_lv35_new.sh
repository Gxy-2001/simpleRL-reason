

RUN_NAME=4_node_Qwen2.5-Math-7B_ppo_from_base_math_lv35_100episodes

python3 openrlhf/cli/train_ppo_ray_box.py \
    --ref_num_nodes 1 \
    --ref_num_gpus_per_node 8 \
    --reward_num_nodes 0 \
    --reward_num_gpus_per_node 0 \
    --critic_num_nodes 1 \
    --critic_num_gpus_per_node 8 \
    --actor_num_nodes 1 \
    --actor_num_gpus_per_node 8 \
    --vllm_num_engines 16 \
    --vllm_tensor_parallel_size 1 \
    --colocate_actor_ref \
    --pretrain /mnt/lyna-selfplay/model/Qwen2.5-Math-7B \
    --save_path /mnt/lyna-selfplay/xy/xy/sft/0205/$RUN_NAME \
    --micro_train_batch_size 2 \
    --train_batch_size 128 \
    --micro_rollout_batch_size 2 \
    --rollout_batch_size 1024 \
    --temperature 0.6 \
    --n_samples_per_prompt 8 \
    --max_samples 100000 \
    --max_epochs 1 \
    --num_episodes 100 \
    --prompt_max_len 1024 \
    --generate_max_len 3000 \
    --zero_stage 3 \
    --bf16 \
    --actor_learning_rate 5e-7 \
    --critic_learning_rate 9e-6 \
    --init_kl_coef 0.01 \
    --prompt_data  data/math_level3to5_data_processed_with_qwen_prompt.json \
    --input_key input \
    --normalize_reward \
    --flash_attn \
    --gradient_checkpointing \
    --save_steps 4 \
    --load_checkpoint \
    --use_wandb 32b598b4cb9a5a9f93d2698fefef0fdbb93cd859 \
    --wandb_project openrlhf_train_ppo2 \
    --wandb_run_name $RUN_NAME \
    --ckpt_path /mnt/lyna-selfplay/xy/xy/sft/0205/$RUN_NAME  \
    --max_ckpt_num 20000

# /mnt/lyna-selfplay/xy/xy/sft/0202/4_node_Qwen2.5-Math-7B_ppo_from_base_math_lv35
# python keepgpu.py