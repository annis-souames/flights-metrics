from stream import S3Consumer
from config import Config

cfg = Config("env")
kafka_cfg = Config("kafka")
aws_cfg = Config("aws")

consumer = S3Consumer(kafka_cfg, aws_cfg)


def run_consumer(event=None, context=None):
    consumer.consume()


run_consumer()
