import yaml
import os

def load_config(config_file="config/paths.yaml"):
    """Carga configuración de rutas desde YAML"""
    config_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", config_file))
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

# Cargar config global
CONFIG = load_config()
PATHS = CONFIG.get('paths', {})
THRESHOLDS = CONFIG.get('thresholds', {})
