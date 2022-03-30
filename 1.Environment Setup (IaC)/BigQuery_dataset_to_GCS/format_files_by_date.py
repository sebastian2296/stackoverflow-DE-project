#!/usr/bin/env python
# coding: utf-8

# In[37]:


from google.cloud import storage
import pandas as pd
import os
import subprocess
import os

# Initialise a client
storage_client = storage.Client("DE-stack-overflow")
# Create a bucket object for our bucket
bucket = storage_client.get_bucket('dtc_data_lake_de-stack-overflow')

# all files in the bucket 
files = list(bucket.list_blobs())
files = [blob.name for blob in files]


# In[58]:


for file in files:
    # Create a blob object from the filepath
    blob = bucket.blob(file)
    # Download the file to a destination
    blob.download_to_filename(file)

    for idx, df in enumerate(pd.read_csv(file, chunksize=1000000)):
        print(f'Processing chunk {idx+1} from {file}')
        try:
            df['group_by_date'] = pd.to_datetime(df['creation_date']).dt.strftime('%Y-%m')
        
        except:
            df['group_by_date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m')
            

        for date in df['group_by_date'].unique():
            df_to_write = df[df['group_by_date']==date]
            output_path=f'{file.split("-")[0]}-{date}.csv'
            df_to_write.to_csv(output_path, mode='a', header=not os.path.exists(output_path), index = False)
            print(f"File {output_path} created succesfully")
            blob_csv = bucket.blob(f"processed/{output_path}")
            blob_csv.upload_from_filename(output_path)
            print(f"File {output_path} uploaded to GCS succesfully")
            
    bashCommand = f"rm {file}"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(f'Finished processing {file}')

os.system('rm *.csv')