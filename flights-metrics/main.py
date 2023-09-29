from api import OpenSkyClient
from config import Config
from loguru import logger

logger.remove()

logger.add("logs.log", rotation="250 MB")

cfg = Config("env")

client = OpenSkyClient(cfg.get("username"), cfg.get("password"))

resp = client.getStatesInRegion(cfg.get("bounding_box"))

print(resp.states)