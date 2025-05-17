import yaml

# Load configuration from YAML
def load_config(config_path):
    """
    Load a YAML configuration file from a given path.

    Args:
        config_path (str): Path to the YAML configuration file to load.

    Returns:
        dict: The loaded configuration as a dictionary.

    Raises:
        FileNotFoundError: If the specified config file doesn't exist.
        yaml.YAMLError: If the YAML file has invalid syntax.
    """
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)