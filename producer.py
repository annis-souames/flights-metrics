from api import FlightRadarClient
from config import Config

from loguru import logger
from stream import RecordsProducer


logger.remove()

# logger.add("/tmp/logs/main.log", rotation="250 MB", retention="2 months")

cfg = Config("env")
kafka_cfg = Config("kafka")

producer = RecordsProducer(kafka_cfg)

client = FlightRadarClient()


# Lambda function to run for producer
def run_producer(event=None, context=None):
    resp = client.getFlightsInRegion(cfg.get("bounding_box"))

    for flight in resp:
        try:
            producer.send(flight)
        except Exception as e:
            # logger.error(f"Error happened while producing a record : {str(e)}")
            continue


run_producer()
