from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_timestamp
from pyspark.sql.avro.functions import from_avro
import json

# Initialize Spark session
spark = SparkSession.builder \
    .appName("AdvertiseX Data Engineering") \
    .getOrCreate()

# Define schema for JSON, CSV, and Avro
ad_impressions_schema = "ad_creative_id STRING, user_id STRING, timestamp STRING, website STRING"
clicks_conversions_schema = "timestamp STRING, user_id STRING, campaign_id STRING, conversion_type STRING"
bid_requests_schema = {
    "type": "record",
    "name": "BidRequest",
    "fields": [
        {"name": "user_id", "type": "string"},
        {"name": "auction_details", "type": "string"},
        {"name": "ad_targeting_criteria", "type": "string"}
    ]
}

# Read ad impressions data (JSON)
ad_impressions_df = spark \
    .readStream \
    .format("json") \
    .schema(ad_impressions_schema) \
    .load("/path/to/ad_impressions")

# Read clicks and conversions data (CSV)
clicks_conversions_df = spark \
    .readStream \
    .format("csv") \
    .schema(clicks_conversions_schema) \
    .option("header", "true") \
    .load("/path/to/clicks_conversions")

# Read bid requests data (Avro)
bid_requests_df = spark \
    .readStream \
    .format("avro") \
    .schema(bid_requests_schema) \
    .load("/path/to/bid_requests")

# Data transformation and enrichment
ad_impressions_df = ad_impressions_df \
    .withColumn("timestamp", to_timestamp(col("timestamp"))) \
    .withColumnRenamed("ad_creative_id", "ad_id")

clicks_conversions_df = clicks_conversions_df \
    .withColumn("timestamp", to_timestamp(col("timestamp")))

# Correlate ad impressions with clicks and conversions
correlated_data = ad_impressions_df \
    .join(clicks_conversions_df, ["user_id"], "inner") \
    .select("ad_id", "user_id", "timestamp", "conversion_type")

# Write processed data to storage
correlated_data.writeStream \
    .format("parquet") \
    .option("path", "/path/to/output") \
    .option("checkpointLocation", "/path/to/checkpoint") \
    .start()

# Error handling and monitoring
def log_error(message):
    kafka_producer.send("error_logs", value=message)

try:
    # Start the stream
    spark.streams.awaitAnyTermination()
except Exception as e:
    log_error(str(e))
    raise

# Stop the Spark session
spark.stop()
