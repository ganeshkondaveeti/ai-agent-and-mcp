import os
import yaml
from typing import Dict, Any
from dotenv import load_dotenv

def load_config(config_path: str = "config/settings.yaml") -> Dict[str, Any]:
    """Load configuration from settings.yaml and environment variables."""
    # Load environment variables from .env
    load_dotenv()
    
    # Load YAML settings
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        
    return config

if __name__ == "__main__":
    # Simple test for exit criteria
    config = load_config()
    print("Config loaded successfully!")
    print(f"App ID: {config['app']['play_store_id']}")
