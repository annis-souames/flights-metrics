import json


class Config:
    _KAFKA_CONFIG_PATH: str = "../config/kafka.json"
    _ENV_CONFIG_PATH: str = "../config/env.json"

    def __init__(self, type: str, path: str = None):
        path = None
        if type == "env" and path is None:
            path = Config._ENV_CONFIG_PATH
        elif type == "kafka" and path is None:
            path = Config._KAFKA_CONFIG_PATH
        else:
            print('Type of config has to either be "env" or "kafka" ')
        with open(path, "rb") as f:
            self.config = json.load(f)

    def get(self, key: str):
        return self.config[key]
