from api import FlightRadarClient
from config import Config
from loguru import logger
from stream import RecordsProducer


logger.remove()

logger.add("logs/main.log", rotation="250 MB", retention="2 months")

cfg = Config("env")
kafka_cfg = Config("kafka")

producer = RecordsProducer(kafka_cfg)

client = FlightRadarClient()


resp = client.getFlightsInRegion(cfg.get("bounding_box"))

print(resp)

for f in resp:
    print(str(f))
    producer.send(f)
