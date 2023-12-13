import yaml

_config = yaml.safe_load(open("teamprojekt_competition_server\server\config.yaml"))

def get_config_value(key):
    return _config[key]