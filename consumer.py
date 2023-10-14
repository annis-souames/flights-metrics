from stream import S3Consumer
from config import Config

cfg = Config("env")
kafka_cfg = Config("kafka")

consumer = S3Consumer(kafka_cfg)


def run_consumer(event=None, context=None):
    consumer.consume()


run_consumer()
