from pyspark.sql import SparkSession
import os

spark = SparkSession \
        .builder \
        .appName('Access GCS') \
        .getOrCreate()

spark._jsc.hadoopConfiguration() \
    .set("google.cloud.auth.service.account.json.keyfile","/.google/credentials/google_credentials_project.json")


BUCKET = os.getenv('GCP_GCS_BUCKET')

#This path has to be dynamically defined for each table
def transform_parquet(table, file_date='*'):
    path=f"gs://{BUCKET}/parquet/{table}-{file_date}.parquet"

    df = spark.read.parquet(path, header=True)
    df.show()

transform_parquet('badges', '2008-08')
