import os
import yaml
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    Loads the configuration from the YAML file.
    
    Args:
        config_path (str): The path to the config file.
        
    Returns:
        dict: The loaded configuration dictionary.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at {config_path}")
        
    with open(config_path, "r", encoding="utf-8") as f:
        try:
            config = yaml.safe_load(f)
            return config
        except yaml.YAMLError as exc:
            print(f"Error parsing YAML config: {exc}")
            raise
