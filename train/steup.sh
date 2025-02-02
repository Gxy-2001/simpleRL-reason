conda create -n openrlhf -y python=3.11
conda init 
source deactivate 
conda activate openrlhf
pip install vllm==0.6.3
pip install -e .


ray start --head --node-ip-address 0.0.0.0 --num-gpus 8
ray start --head --node-ip-address=$(hostname -I | awk '{print $1}') --port=6379 --num-gpus=8
