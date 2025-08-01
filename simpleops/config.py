# simpleops/config.py
import yaml
from pathlib import Path

CONFIG_FILE = Path.home() / ".simpleops" / "config.yaml"

def load_config():
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Config not found: {CONFIG_FILE}\n"
            "Run:\n"
            "  mkdir -p ~/.simpleops && echo 'environments: {dev: {aws: {region: us-east-1, profile: simpleops-dev}}}' > ~/.simpleops/config.yaml"
        )
    with open(CONFIG_FILE, 'r') as f:
        return yaml.safe_load(f)
