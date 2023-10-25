from config import Config
from kafka import KafkaConsumer
from loguru import logger
import json
import boto3
from datetime import datetime


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
            consumer_timeout_ms=kafkaConfig.get(
                "consumer_timeout"
            ),  # Default : Timeout after 3 seconds
        )

        self.awsAccessKeyID = awsConfig.get("aws_access_key_id")
        self.awsAccessKeySecret = awsConfig.get("aws_access_key_secret")
        self.awsSessionToken = awsConfig.get("aws_session_token")
        self.bucket = awsConfig.get("s3")["bucket"]
        self.s3Prefix = awsConfig.get("s3")["prefix"]
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=self.awsAccessKeyID,
            aws_secret_access_key=self.awsAccessKeySecret,
        )

        # This is called once per invocation, creates new partition folder for efficient crawling
        self.currentPrefix = self.createPartitionFolder()

    def createPartitionFolder(self):
        # Get the current date and time as a string
        current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M")

        # Construct the full path for the new subfolder
        new_folder_path = f"{self.s3Prefix}/{current_datetime}/"

        # Create the subfolder in the S3 bucket
        self.s3.put_object(Bucket=self.bucket, Key=new_folder_path)
        logger.info(f"Created new partition folder {new_folder_path}")
        return new_folder_path

    def uploadToS3(self, data: dict):
        # Assuming 'data' is a JSON object
        data_json = json.dumps(data)

        # Construct S3 object key based on your requirements
        s3_object_key = f"{self.currentPrefix}flight_{data['id']}.json"
        self.s3.put_object(Bucket=self.bucket, Key=s3_object_key, Body=data_json)
        logger.success(f"Uploaded {s3_object_key} to S3 bucket")

    def consume(self, withS3: bool = True):
        msg_counter, put_counter = 0, 0
        for msg in self.consumer:
            if put_counter >= 50:
                break
            try:
                msg_counter += 1
                if withS3:
                    self.uploadToS3(msg.value)
                    put_counter += 1
            except Exception as e:
                logger.error(f"An error occured {str(e)}")
        self.consumer.close()
        logger.info(
            f"Consumer ended, it consumed and uploaded {put_counter} out of {msg_counter} records successfully."
        )
