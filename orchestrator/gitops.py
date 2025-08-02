import yaml
import git
from pathlib import Path

REPO_PATH = Path(__file__).resolve().parent.parent  # Root project dir

def update_replicas(edge_replicas, cloud_replicas):
    # Load and modify Edge YAML
    edge_file = REPO_PATH / 'deploy/edge/deployment.yaml'
    cloud_file = REPO_PATH / 'deploy/cloud/deployment.yaml'

    with open(edge_file, 'r') as f:
        edge_yaml = yaml.safe_load(f)
    edge_yaml['spec']['replicas'] = edge_replicas
    with open(edge_file, 'w') as f:
        yaml.dump(edge_yaml, f)

    # Load and modify Cloud YAML
    with open(cloud_file, 'r') as f:
        cloud_yaml = yaml.safe_load(f)
    cloud_yaml['spec']['replicas'] = cloud_replicas
    with open(cloud_file, 'w') as f:
        yaml.dump(cloud_yaml, f)

    # Git commit and push
    repo = git.Repo(REPO_PATH)
    repo.git.add(update=True)
    repo.index.commit(f"orchestrator: move app to {'cloud' if cloud_replicas else 'edge'}")
    origin = repo.remote(name='origin')
    origin.push()
