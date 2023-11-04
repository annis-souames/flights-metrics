# ✈️ Flights-Metrics


Flights Metrics is a data pipeline that aim to provide hourly analytics on flights over a city or a region (London is the default configuration). The pipeline is built in Python and deployed on several AWS services : Lambda, S3, Glue and Athena. 

## Preview

![architecture](docs/flights-metrics-architecture.png)



## Architecture

The project is deployed fully only on AWS, except for the Kafka broker which is hosted on the free tier of Upstash. Metabase is deployed on Amazon Lightsail as a Docker container. Flights are fetched every 15 minutes with a Lambda function and consumed every hour by another Lambda function, Apache Kafka serves both as a streaming layer and a buffer in this case. 

The consumer creates partitions in Athena (see note) and the Metabase dashboard performs different SQL queries to retrieve the metrics data from Athena. Data is kept for 3 days in S3 and then it's automatically deleted through an S3 lifecycle policy to reduce costs.

![architecture](docs/flights-metrics-architecture.png)

**Note:** The old architecture was using Glue to automate the process of adding new partitions from S3 to Athena, however, this approach was expensive and we developed a new method in `stream/S3Consumer.py` to add partitions to S3 directly using an Athena query, this reduces costs by over **60%**!

## Deploying to Lamba

Currently, we have two different bash scripts to generate the zip files to be uploaded on AWS lambda: `vendor.zip` for dependencies and `package.zip` for both the producer and consumer functions.

```bash
# To package the libraries into one zip run :
bash package-deps.sh
```

```bash
# To package the app into one zip run :
bash package-deps.sh
```

## Improvements for the future

- Implement a CI/CD pipeline with Github Actions and AWS SAM to automate the deployment of new versions.
- Add an ETL function to convert JSON files to Parquet for more efficient analytics.
- Cache some parts of the dashboard hourly to reduce the number of requests and costs. 

