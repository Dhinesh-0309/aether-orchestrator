import time
import yaml
from orchestrator.metrics import get_cpu_usage
from orchestrator.decision_engine import make_decision
from orchestrator.gitops import update_replicas


def load_config():
    with open("configs/settings.yaml", "r") as f:
        return yaml.safe_load(f)

def run():
    config = load_config()
    while True:
        cpu = get_cpu_usage(config["prometheus_url"])
        decision = make_decision(cpu, config["cpu_threshold"])
        print(f"[INFO] CPU: {cpu}%, Decision: {decision}")

        if decision == "cloud":
            print("[ACTION] Moving workload to cloud...")
            update_replicas(edge_replicas=0, cloud_replicas=1)
        elif decision == "edge":
            print("[ACTION] Ensuring workload runs on edge...")
            update_replicas(edge_replicas=1, cloud_replicas=0)

        time.sleep(config["poll_interval"])
