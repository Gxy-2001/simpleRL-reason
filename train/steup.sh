# conda create -n openrlhf -y python=3.11
# conda init 
# source deactivate 
# conda activate openrlhf
# pip install vllm==0.6.3
# pip install -e .


# # ray start --head --node-ip-address 0.0.0.0 --num-gpus 8
# # ray start --head --node-ip-address=$(hostname -I | awk '{print $1}') --port=6379 --num-gpus=8
# # 10.6.64.195:6379
# ray start --address=10.6.64.195:6379 --num-gpus=8

ray job submit --address="http://127.0.0.1:8265" \
    -- bash examples/script/train_ppo_qwen_base_math_lv35_new.sh
