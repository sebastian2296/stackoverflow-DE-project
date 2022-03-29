As a first step, and given that our data is part of BigQuery public datasets,
we will export the table `posts_questions` to our datalake in Google Cloud Storage.

We will use that bucket as our source to automate pulling the data in batches (schedule interval to be defined). This first pipeline would format our data to parquet and as a last step will upload it to another bucket. 

From this last bucket, we will create our BigQuery tables to partion and cluster them.