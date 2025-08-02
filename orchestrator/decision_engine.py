def make_decision(cpu_usage, threshold):
    if cpu_usage > threshold:
        return "cloud"
    else:
        return "edge"
