from config import Config
from kafka import KafkaConsumer
from loguru import logger
import json
import boto3
from datetime import datetime
import sys


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
        self.athena = boto3.client(
            "athena",
            aws_access_key_id=self.awsAccessKeyID,
            aws_secret_access_key=self.awsAccessKeySecret,
            region_name="eu-west-2",
        )

        # This is called once per invocation, creates new partition folder for efficient crawling
        self.currentPrefix = self.createPartitionFolder()
        self.s3URI = f"s3://{self.bucket}/{self.currentPrefix}"
        self.athenaOutputLocation = awsConfig.get("athena")["output"]

    def createPartitionFolder(self):
        # Get the current date and time as a string
        current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M")

        # Construct the full path for the new subfolder
        new_folder_path = f"{self.s3Prefix}/{current_datetime}/"

        # Create the subfolder in the S3 bucket
        self.s3.put_object(Bucket=self.bucket, Key=new_folder_path)
        logger.info(f"Created new partition folder {new_folder_path}")
        return new_folder_path

    # This method will update partitions without using Glue
    def updateAthenaPartition(self):
        folderName = self.s3URI.split("/")[-2].strip("/")
        query = f"""ALTER TABLE flights.main ADD
                    PARTITION (dt = '{folderName}') 
                    LOCATION '{self.s3URI}';"""
        try:
            self.athena.start_query_execution(
                QueryString=query,
                ResultConfiguration={"OutputLocation": self.athenaOutputLocation},
            )
        except Exception as e:
            logger.error(f"Couldn't add partition to Athena {folderName}: {e}")
            sys.exit(1)
        else:
            logger.success(f"Added partition {folderName} to Athena")

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
            try:
                msg_counter += 1
                if withS3:
                    self.uploadToS3(msg.value)
                    put_counter += 1
            except Exception as e:
                logger.error(f"An error occured {str(e)}")
        self.consumer.close()
        self.updateAthenaPartition()
        logger.info(
            f"Consumer ended, it consumed and uploaded {put_counter} out of {msg_counter} records successfully."
        )
