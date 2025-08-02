from orchestrator.gitops import update_replicas

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
            print("[ACTION] Ensuring workload is on edge...")
            update_replicas(edge_replicas=1, cloud_replicas=0)

        time.sleep(config["poll_interval"])
