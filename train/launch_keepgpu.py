import ray
import subprocess
from ray.util.scheduling_strategies import NodeAffinitySchedulingStrategy

# 连接到集群（如果在 head 节点上运行脚本，可以用 address="auto"）
ray.init(address="auto")

@ray.remote(num_gpus=1)
def run_keepgpu():
    # 调用系统命令运行 keepgpu.py
    # 如果需要使用绝对路径，请相应调整
    subprocess.run(["python", "keepgpu.py"], check=True)

# 获取当前集群中的所有节点信息
nodes = ray.nodes()

jobs = []
for node in nodes:
    # 只选择状态为 ALIVE 的节点
    if node["Alive"]:
        node_id = node["NodeID"]
        # 指定调度策略，让任务只能调度到该节点
        strategy = NodeAffinitySchedulingStrategy(node_id=node_id, soft=False)
        job = run_keepgpu.options(scheduling_strategy=strategy).remote()
        jobs.append(job)

# 等待所有任务执行完成
ray.get(jobs)
print("所有节点上的 keepgpu.py 均已启动。")
