from api import OpenSkyClient
from config import Config


cfg = Config("env")

client = OpenSkyClient()

resp = client.getStatesInRegion(cfg.get("bounding_box"))

print(resp)