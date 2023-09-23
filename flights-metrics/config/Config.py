import json


class Config():
    def __init__(self, path: str):
        with open(path, "rb") as f:
            self.config = json.load(f)

    def get(self, key: str):
        return self.config[key]
    