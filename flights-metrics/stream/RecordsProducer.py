import json
from kafka import KafkaProducer, KafkaConsumer
from loguru import logger


class RecordsProducer:
    def __init__(self, config: dict):
        self.topic = (config["topic"],)
        self.server = config["bootstrap_server"]
        self.producer = KafkaProducer(
            value_serializer=lambda m: json.dumps(m).encode("ascii"),
            bootstrap_servers=[config["topic"]],
            retries=config["max_retries"],
        )

    def send(self, msg: dict):
        # produce asynchronously with callbacks
        self.producer.send("my-topic", msg).add_callback(
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
