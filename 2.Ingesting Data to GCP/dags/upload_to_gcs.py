from google.cloud import storage

def upload_to_gcs(file_):
    # Initialise a client
    storage_client = storage.Client("DE-stack-overflow")
    # Create a bucket object for our bucket
    bucket = storage_client.get_bucket('dtc_data_lake_de-stack-overflow')
    blob = bucket.blob(f'parquet/{file_}')
    blob.upload_from_filename(file_)
