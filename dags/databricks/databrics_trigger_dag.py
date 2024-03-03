from datetime import datetime

from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
}

# Define the DAG
dag = DAG(
    'databricks_trigger_dag',
    default_args=default_args,
    description='Run Databricks notebook with parameters',
    schedule=None,
    params={
        "country": "IND",
        "week": 2
    }
)

# Define the notebook task
notebook_task = DatabricksRunNowOperator(
    task_id='run_databricks_notebook',
    databricks_conn_id='databricks_default',  # Connection ID to Databricks
    job_id="1061107672020870",  # Job ID of the notebook
    dag=dag,
    notebook_params={"country": "{{params.country}}", "week": "{{params.week}}"}  # Parameters to pass to the notebook
)

# Set task dependencies
notebook_task
