from stream import S3Consumer
from config import Config

cfg = Config("env")
kafka_cfg = Config("kafka")
aws_cfg = Config("aws")


def run_consumer(event=None, context=None):
    consumer = S3Consumer(kafka_cfg, aws_cfg)
    consumer.consume()


# run_consumer()
