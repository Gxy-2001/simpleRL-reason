SCRIPT=$1
WANDB_KEY=$2


python3 -m pip install -e .
python3 -m pip install word2number


ray stop
PORT=65533
NODE_N=$(cat ~/hostfile | wc -l)
IP=$(hostname -I | awk '{print $1}')
CURRENT_DIR=$(pwd)
for i in $(seq 0 $((NODE_N-1)));
do
    if [ $i -eq 0 ]; then
        echo ">>> process: $i (head)"
        ray start --head --port=$PORT
    else
        echo ">>> process: $i"
        ssh  node-${i} "cd $CURRENT_DIR && ray start --address=$IP:$PORT"
    fi
done
echo ">>> ray started"


ray job submit --address="http://127.0.0.1:8265" \
        --runtime-env-json='{
        "pip": ["ray==2.12.0", "latex2sympy2", "timeout_decorator"]
    }' -- /bin/bash $SCRIPT $WANDB_KEY


ray stop
cd /home/aiscuser/amlt-code-download/job/auto_occupy
bash auto_occupy_single_node.sh ./
