from config import Config
from kafka import KafkaConsumer
from loguru import logger
import json
import boto3


class S3Consumer:
    def __init__(self, kafkaConfig: Config, awsConfig: Config):
        self.topic = kafkaConfig.get("topic")
        self.consumer = KafkaConsumer(
            self.topic,
            group_id="$GROUP_NAME",
            bootstrap_servers=[kafkaConfig.get("bootstrap_server")],
            security_protocol=kafkaConfig.get("security_protocol"),
            sasl_mechanism=kafkaConfig.get("sasl_mechanism"),
            sasl_plain_username=kafkaConfig.get("username"),
            sasl_plain_password=kafkaConfig.get("password"),
            auto_offset_reset="earliest",
            value_deserializer=lambda m: json.loads(m.decode("ascii")),
        )

        self.awsAccessKeyID = awsConfig.get("aws_access_key_id")
        self.awsAccessKeySecret = awsConfig.get("aws_access_key_secret")
        self.bucket = awsConfig.get("s3")["bucket"]
        self.s3Prefix = awsConfig.get("s3")["prefix"]

    def uploadToS3():
        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

        # Assuming 'data' is a JSON object
        data_json = json.dumps(data)

        # Construct S3 object key based on your requirements
        s3_object_key = f"{S3_PREFIX}flight_{data['flight_id']}.json"

        s3.put_object(Bucket=S3_BUCKET_NAME, Key=s3_object_key, Body=data_json)
        print(f"Uploaded data to S3: {s3_object_key}")

    def consume(self, withS3: bool = True):
        for msg in self.consumer:
            logger.info(msg.value)
