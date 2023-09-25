from api import OpenSkyClient
from config import Config


cfg = Config("env")

client = OpenSkyClient(cfg.get("username"), cfg.get("password"))

resp = client.getStatesInRegion(cfg.get("bounding_box"))

print(resp.states)