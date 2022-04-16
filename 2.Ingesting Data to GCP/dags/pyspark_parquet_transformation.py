# Posts-questions and Posts-answers "schema"
from pyspark.sql.functions import col
from pyspark.sql import types, SparkSession
# from pyspark import SparkConf, SparkContext
import sys
import os

def implement_schema(df, table):
    if table in ['posts_questions', 'posts_answers']:
        df2 = df.withColumn('id',col('id').cast(types.IntegerType())) \
                .withColumn('title',col('title').cast(types.StringType())) \
                .withColumn('body',col('body').cast(types.StringType())) \
                .withColumn('accepted_answer_id',col('accepted_answer_id').cast(types.IntegerType())) \
                .withColumn('answer_count',col('answer_count').cast(types.IntegerType())) \
                .withColumn('comment_count',col('comment_count').cast(types.IntegerType())) \
                .withColumn('community_owned_date',col('community_owned_date').cast(types.TimestampType())) \
                .withColumn('creation_date',col('creation_date').cast(types.TimestampType())) \
                .withColumn('favorite_count',col('favorite_count').cast(types.IntegerType())) \
                .withColumn('last_activity_date',col('last_activity_date').cast(types.TimestampType())) \
                .withColumn('last_edit_date',col('last_edit_date').cast(types.TimestampType())) \
                .withColumn('last_editor_user_id',col('last_editor_user_id').cast(types.IntegerType())) \
                .withColumn('last_editor_display_name',col('last_editor_display_name').cast(types.StringType())) \
                .withColumn('owner_display_name',col('owner_display_name').cast(types.StringType())) \
                .withColumn('owner_user_id',col('owner_user_id').cast(types.IntegerType())) \
                .withColumn('parent_id',col('parent_id').cast(types.IntegerType())) \
                .withColumn('post_type_id',col('post_type_id').cast(types.IntegerType())) \
                .withColumn('score',col('score').cast(types.IntegerType())) \
                .withColumn('tags',col('tags').cast(types.StringType())) \
                .withColumn('view_count',col('view_count').cast(types.IntegerType())) \
                .withColumn('group_by_date',col('group_by_date').cast(types.TimestampType()))
        
    if table == 'badges':
        df2 = df.withColumn('id',col('id').cast(types.IntegerType())) \
                .withColumn('name',col('name').cast(types.StringType())) \
                .withColumn('date',col('date').cast(types.TimestampType())) \
                .withColumn('user_id',col('user_id').cast(types.IntegerType())) \
                .withColumn('class',col('class').cast(types.IntegerType())) \
                .withColumn('tag_based',col('tag_based').cast(types.BooleanType(),)) \
                .withColumn('group_by_date',col('group_by_date').cast(types.TimestampType())) \
        
    if table == 'users':
        df2 = df.withColumn('id',col('id').cast(types.IntegerType())) \
                .withColumn('display_name',col('display_name').cast(types.StringType())) \
                .withColumn('about_me',col('about_me').cast(types.StringType())) \
                .withColumn('age',col('age').cast(types.IntegerType())) \
                .withColumn('creation_date',col('creation_date').cast(types.TimestampType())) \
                .withColumn('last_access_date',col('last_access_date').cast(types.TimestampType(),)) \
                .withColumn('location',col('location').cast(types.StringType())) \
                .withColumn('reputation',col('reputation').cast(types.IntegerType())) \
                .withColumn('up_votes',col('up_votes').cast(types.IntegerType())) \
                .withColumn('down_votes',col('down_votes').cast(types.IntegerType())) \
                .withColumn('views',col('views').cast(types.IntegerType())) \
                .withColumn('profile_image_url',col('profile_image_url').cast(types.StringType(),)) \
                .withColumn('website_url',col('website_url').cast(types.StringType())) \
                .withColumn('group_by_date',col('group_by_date').cast(types.TimestampType())) \
            
    return df2

#This path has to be dynamically defined for each table
def transform_parquet(table, file_date='*'):
    path=f"gs://{BUCKET}/parquet/{table}-{file_date}.parquet"

    df = spark.read.parquet(path, header=True)
    df = implement_schema(df, table)
    
    df.repartition(4).write.format("parquet").mode("overwrite").save(f"gs://{BUCKET}/BigQuery/{table}-{file_date}")
    

spark = SparkSession.builder.master("local[*]")\
        .appName('Modidy Schema')\
        .getOrCreate()

spark._jsc.hadoopConfiguration() \
    .set("google.cloud.auth.service.account.json.keyfile","/.google/credentials/google_credentials_project.json")


BUCKET = os.getenv('GCP_GCS_BUCKET')



table_name = sys.argv[1]
file_date = sys.argv[2]

transform_parquet(table_name, file_date)

