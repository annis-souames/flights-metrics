from api import OpenSkyClient
from config import Config
from loguru import logger
from stream import RecordsProducer


logger.remove()

logger.add("logs/main.log", rotation="250 MB", retention="2 months")

cfg = Config("env")
kafka_cfg = Config("kafka")

producer = RecordsProducer(kafka_cfg)

client = OpenSkyClient(cfg.get("username"), cfg.get("password"))


resp = client.getStatesInRegion(cfg.get("bounding_box"))

print(resp.states)

producer.send(resp, "flights")
