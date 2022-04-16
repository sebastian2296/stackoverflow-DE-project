from airflow import DAG
from datetime import datetime
from airflow.utils.task_group import TaskGroup
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator, BigQueryInsertJobOperator
from airflow.utils.dates import days_ago
import os
from google.cloud import storage

storage_client = storage.Client("DE-stack-overflow")
bucket = storage_client.get_bucket('dtc_data_lake_de-stack-overflow')
files = list(bucket.list_blobs())
files = [blob.name for blob in files if 'BigQuery/' in blob.name]
files = [file for file in files if '.parquet' in file]

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
tables = ['badges', 'posts_questions', 'posts_answers', 'users']

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")

BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'stack_overflow_data')
CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
DATASET = "stack_overflow_data"
INPUT_PART = "BigQuery"
INPUT_FILETYPE = "parquet"
PARTITION_COL = 'creation_date'


with DAG('load_to_BigQuery', start_date=days_ago(0), schedule_interval="@once", catchup=True, concurrency=20, max_active_runs=4) as \
dag: 
    for table in tables:

        uris = [f'gs://{BUCKET}/'+ file for file in files if table in file]


        CREATE_BQ_TBL_QUERY = (
        f"CREATE OR REPLACE TABLE {BIGQUERY_DATASET}.{table}_{DATASET}_partitioned \
        PARTITION BY DATE(group_by_date) \
        AS \
        SELECT * FROM {BIGQUERY_DATASET}.{table}_{DATASET}_external_table;"
    )



        with TaskGroup(f'create_external_{table}') as processing_tasks:


            bigquery_external_table_task = BigQueryCreateExternalTableOperator(
                task_id=f"create_{table}_{DATASET}_external_table",
                table_resource={
                    "tableReference": {
                        "projectId": PROJECT_ID,
                        "datasetId": BIGQUERY_DATASET,
                        "tableId": f"{table}_{DATASET}_external_table",
                    },
                    "externalDataConfiguration": {
                        "autodetect": "True",
                        "sourceFormat": f"{INPUT_FILETYPE.upper()}",
                        "sourceUris": uris,
                    },
                },
            )

            # Create a partitioned table from external table
            bq_create_partitioned_table_job = BigQueryInsertJobOperator(
                task_id=f"bq_create_{table}_{DATASET}_partitioned_table_task",
                configuration={
                    "query": {
                        "query": CREATE_BQ_TBL_QUERY,
                        "useLegacySql": False,
                    }
                }
            )


            bigquery_external_table_task >> bq_create_partitioned_table_job

