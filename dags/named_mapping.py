import datetime as dt

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# named-mapping workflow dag

with DAG(
        dag_id="named-mapping-example",
        schedule=None,
        start_date=dt.datetime(year=2022, month=10, day=27),
        end_date=None,
        tags=["learning", "examples", "named-mapping"]
) as named_mapping_workflow_dag:
    def get_countries():
        return [{"country_name": "IND"}, {"country_name": "USA"}, {"country_name": "CAN"}, {"country_name": "GBR"},
                {"country_name": "FRA"}, {"country_name": "ITA"}, {"country_name": "DEU"}, {"country_name": "AUS"},
                {"country_name": "BRA"}, {"country_name": "MEX"}]


    get_counties = PythonOperator(dag=named_mapping_workflow_dag, task_id="get_countries",
                                  python_callable=get_countries, do_xcom_push=True)

    print_country_name = BashOperator.partial(dag=named_mapping_workflow_dag,
                                              task_id="print_country_name",
                                              bash_command='echo "Processing country: {{task.env.country_name}}"'
                                              ).expand(env=get_counties.output)

    print_country_name_with_named_mapping = BashOperator.partial(dag=named_mapping_workflow_dag,
                                                                 task_id="print_country_name_with_named_mapping",
                                                                 bash_command='echo "Processing country: {{'
                                                                              'task.env.country_name}}"',
                                                                 map_index_template="{{task.env.country_name}}"
                                                                 ).expand(env=get_counties.output)

    get_counties >> [print_country_name, print_country_name_with_named_mapping]
