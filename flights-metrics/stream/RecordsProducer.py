import json
from kafka import KafkaProducer, KafkaConsumer
from loguru import logger
from config import Config


class RecordsProducer:
    def __init__(self, config: Config):
        print(config)
        self.topic = config.get("topic")
        self.server = config.get("bootstrap_server")
        self.producer = KafkaProducer(
            value_serializer=lambda m: json.dumps(m).encode("ascii"),
            bootstrap_servers=[config.get("bootstrap_server")],
            retries=config.get("max_retries"),
            sasl_mechanism=config.get("sasl_mechanism"),
            sasl_plain_username=config.get("username"),
            sasl_plain_password=config.get("password"),
        )
        print(self.producer.bootstrap_connected())

    def send(self, msg: dict):
        # produce asynchronously with callbacks
        self.producer.send(self.topic, msg).add_callback(
            self._on_send_success
        ).add_errback(self._on_send_error)
        self.producer.flush()


def _on_send_success(record_metadata):
    logger.info(
        f"Record was successfully sent to Kafka in partition #{record_metadata.partition}"
    )


def _on_send_error(excp):
    logger.error(f"Could not send msg : {excp}")
    # handle exception