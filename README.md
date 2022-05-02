# Problem 

This project aims to show some interesting statistics of the Stack-Overflow's
public dataset in BigQuery. 

Some of the questions answered (taken from google cloud page): 

* What is the percentage of questions that have been answered over the years?
* What is the reputation and badge count of users across different tenures on StackOverflow?
* What are 10 of the “easier” gold badges to earn?
* Which day of the week has most questions answered within an hour?

# Dataset

The dataset in which all transformations and analysis will be developed is the 
Stack Overflow public dataset from BigQuery. Given that this dataset is already
in a datawarehouse, there's an additional step/pipeline run as first step to 
transfer these data (by month) from BigQuery to GCS in csv format.

From then on, the csv files are transformed into parquet format, taken to the datawarehouse in partitioned tables and ultimately transformed to answer the questions mentioned in the previous section. 

# Project Details

Some of the technologies used in this project are:

*  **Google Cloud Platform**: to storage raw data in GCS (data lake) and to analyze it in BigQuery.
*  **Terraform**: Tool that provides Infraestructure as Code (IaC) to generate our resources in the cloud (buckets and datasets).
* **Airflow**: to orchestrate our data pipelines in a monthly schedule.
* **Spark**: A distributed processing engine that allows us to make complex transformations to the raw data (we mainly use the SQL API).

# How to reproduce this project?

Clone the repo into your local using  `git clone https://github.com/sebastian2296/stackoverflow-DE-project.git`

## 1. Environment Setup

As we mentioned earlier, first we need to transfer the StackOverflow dataset, which is stored in Bigquery  into a bucket. To do that, we should follow these steps:

**1**. Create a project called `DE-stack-overflow` in GCP and create a *Service Account* with these permissions:
- `BigQuery Admin`
- `Storage Admin`
- `Storage Object Admin`
- `Viewer`

Download the Service Account json file, rename it to `google_credentials_project.json` and store it in `$HOME/.google/credentials/` .

Also make sure that these APIs are activated:
* https://console.cloud.google.com/apis/library/iam.googleapis.com
* https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com


**2**. Add Credentials Environment Variable to `.bashrc` file

Create  `GOOGLE_APPLICATION_CREDENTIALS` environment varaible and link it to your credentials path (`$HOME/.google/credentials/` ).

- Add to your  `.bashrc` configuration file the following line (at the end):
    ```sh
    export GOOGLE_APPLICATION_CREDENTIALS=$HOME/.google/credentials/google_credentials_project.json
    ```

**3**. cd into `1.Environment Setup (Iac)/terraform_setup` folder and run the following commnands:

* **Initialize terraform**:
	```sh
	 terraform init
* **Check that you're creating the correct resources (GCS bucket and BigQuery dataset)**:
    ```sh
    terraform plan
    ```
* **Create the resources**:
    ```sh
    terraform apply
    ```

**4**. cd into `1.Environment Setup (Iac)/BigQuery_dataset_to_GCS` and run the scripts in the following order:

- `python3 bq_dataset_to_GCS.py` to transfer uneven csv files into our bucket.
- `python3 format_files_by_date.py`to group our data by month and year in csv files.

**Important Note**: At the end of this step, it is necessary to make our [bucket of public](https://cloud.google.com/storage/docs/access-control/making-data-public) access so that we can download the csv files using our Airflow Dags. 

## 2. Ingest Data to GCP Bucket

**1**.  cd into the folder `Ingest Data to GCP`
- Create .env file by using `echo -e "AIRFLOW_UID=$(id -u)" > .env`
-  Build your docker environment using `docker-compose build`
-  Initialize de Airflow db with `docker-compose up airflow-init`
-  Run Airflow with `docker-compose up -d`

**2**. Run the Dag by triggering manually from Airflow's UI.

## 3. Moving data into the DataWarehouse (BigQuery)

**1**. cd into the folder `3. Moving data to DWH`:
- Run `docker-compose build` 
- Use `docker-compose up airflow-init` to initialize airflow's database.
- Run `docker-compose up -d` to inialiaze Airflow as well as Jupyter.

**2**. Trigger the Dag manually from Airflow's UI. This DAG moves data from our GCS bucket (parquet files) into BigQuery. We should end up with partitioned tables by month
for each one of our datasets: `badges`, `posts_questions`,`posts_answers` and `users`. 

**Note**: The reasoning behind using date to partion our tables is that our queries usually filter by date, and this makes retrieving our data more efficient/less costly.

**3**.  Inspect the notebook `dashboard_views.ipynb` and run the cells to generate the necessary transformations to answer the questions provided in the [Problem](#Problem) section.

# Dashboard

![alt text](https://github.com/sebastian2296/stackoverflow-DE-project/blob/main/img/1_dashboard.PNG)

![alt text](https://github.com/sebastian2296/stackoverflow-DE-project/blob/main/img/2_dashboard.PNG)

You can check the dashboard [here](https://datastudio.google.com/reporting/d2fa6d93-faf8-4243-aacf-4cd29f3ae7e7)


Special thanks to [DataTalks](https://datatalks.club/) Club for making an awesome [Data Engineering Course](https://github.com/DataTalksClub/data-engineering-zoomcamp) :) 
