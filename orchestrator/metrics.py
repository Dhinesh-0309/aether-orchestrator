import requests

def get_cpu_usage(prometheus_url):
    try:
        query = '100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)'
        response = requests.get(f"{prometheus_url}/api/v1/query", params={'query': query})
        value = float(response.json()["data"]["result"][0]["value"][1])
        return round(value, 2)
    except Exception as e:
        print(f"[ERROR] Failed to fetch CPU usage: {e}")
        return 0.0
