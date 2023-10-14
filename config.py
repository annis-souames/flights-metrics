import json
from loguru import logger


class Config:
    _KAFKA_CONFIG_PATH: str = "config/kafka.json"
    _ENV_CONFIG_PATH: str = "config/env.json"
    _AWS_CONFIG_PATH: str = "config/aws.json"

    def __init__(self, type: str, path: str = None):
        configFiles = {
            "env": Config._ENV_CONFIG_PATH,
            "kafka": Config._KAFKA_CONFIG_PATH,
            "aws": Config._AWS_CONFIG_PATH,
        }
        self.path = path
        if self.path is None:
            self.path = configFiles[type]

        if type not in configFiles.keys():
            logger.error('Type of config has to either be "env" or "kafka" ')

        if self.path is None:
            self.path = configFiles[type]

        with open(self.path, "rb") as f:
            self.config = json.load(f)

    def get(self, key: str):
        return self.config[key]
