from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
from format_to_parquet import parquetize
from airflow.utils.task_group import TaskGroup
from upload_to_gcs import upload_to_gcs
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
import os


AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
tables = ['badges', 'posts_questions', 'posts_answers', 'users']


URL_PREFIX = 'https://storage.googleapis.com/dtc_data_lake_de-stack-overflow/processed/'


with DAG('IngestToGCP', start_date=datetime(2008, 7, 1), schedule_interval="0 0 1 * *", catchup=True, concurrency=20, max_active_runs=4) as \
dag: 
    for table in tables:

        URL_TEMPLATE = URL_PREFIX + table +'-{{execution_date.strftime(\'%Y-%m\')}}.csv'
        OUTPUT_FILE_TEMPLATE = AIRFLOW_HOME + f'/{table}'+'-{{execution_date.strftime(\'%Y-%m\')}}.csv'
        FILE_NAME = table +'-{{execution_date.strftime(\'%Y-%m\')}}.csv'
        PARQUET_TEMPLATE = FILE_NAME.replace('.csv', '.parquet')

        with TaskGroup(f'processing_tasks_{table}') as processing_tasks:

            wget_task = BashOperator(
                task_id=f'download_files_{table}',
                bash_command=f'curl -A "Mozilla Chrome Safari" -sSfl --connect-timeout 5 \
                    --retry 5 \
                    {URL_TEMPLATE} > {OUTPUT_FILE_TEMPLATE}'
            ) 

            format_to_parquet = PythonOperator(
                task_id = f'format_to_parquet_{table}',
                python_callable =parquetize,
                op_kwargs = dict(src_file=FILE_NAME,
                path=f'{AIRFLOW_HOME}/{PARQUET_TEMPLATE}')
            )
        
            remove_csv = BashOperator(
                task_id=f'remove_{table}_csv',
                bash_command=f'rm {OUTPUT_FILE_TEMPLATE}'
            )

            ingest_to_gcs = PythonOperator(
                task_id=f'ingest_{table}_to_bucket',
                python_callable=upload_to_gcs,
                op_kwargs=dict(file_=PARQUET_TEMPLATE)
            )


            spark_job = SparkSubmitOperator(
                task_id="spark_job",
                application="./dags/pyspark_parquet_transformation.py", # Spark application path created in airflow and spark cluster
                name="format_schema",
                conn_id="spark_project",
                verbose=1,
                conf={"spark.master":"local[*]"},
                application_args=[table, "{{ execution_date.strftime(\'%Y-%m\') }}"],
                dag=dag)

            remove_parquet = BashOperator(
                task_id=f'remove_{table}_parquet',
                bash_command=f'rm {AIRFLOW_HOME}/{PARQUET_TEMPLATE}'
            )

            [wget_task >> format_to_parquet] >> remove_csv >> ingest_to_gcs >> spark_job  >> remove_parquet

