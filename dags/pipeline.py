from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd
import requests
import psycopg2



def fetch_data(start_date, end_date): 
    API_URL  = "https://earthquake.usgs.gov/fdsnws/event/1/query"

    params = {
        "format": "geojson",
        "starttime": start_date,
        "endtime": end_date,
    }
    response = requests.get(API_URL, params=params)
    data = response.json()
    print(len(data['features']))
    print(data['features'][0])
    print(data['features'][-1])
    data = data['features']

    return data


def store_data(data):
    # Connect to PostgreSQL
    # Fetch the password from environment variables
    db_password = os.getenv("DB_PASSWORD")
        
    # Connect to PostgreSQL
    conn = psycopg2.connect("dbname=earthquake_db user=postgres password=db_password host=localhost")


    cursor = conn.cursor()
    print('connection to the db established')
    for feature in data:
        props = feature['properties']
        
        if props['mag']>2:
            geometry = feature['geometry']['coordinates']
            cursor.execute("""
                INSERT INTO earthquakes (earthquake_id, magnitude, depth, latitude, longitude, location, time)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (earthquake_id) DO NOTHING;
            """, (
                feature['id'], props['mag'], geometry[2], geometry[1], geometry[0],
                props['place'], datetime.fromtimestamp(props['time'] / 1000)
            ))

    conn.commit()
    print(f"Today's Earthquake data saved in the earthquake table")

    cursor.close()
    conn.close()
    print('connection to the db closed')


dag = DAG(
    'pipeline_earthquake_data',
    description='Earthquake data pipeline hourly update',
    schedule_interval='@hourly',
    start_date=datetime.utcnow(),
)

# Define the tasks in the DAG
task_fetch_earthquake_data = PythonOperator(
    task_id='fetch_earthquake_data',
    python_callable=fetch_data,
    dag=dag
)


task_store_to_db = PythonOperator(
    task_id='store_to_db',
    python_callable=store_data,
    op_kwargs={'data': '{{ ti.xcom_pull(task_ids="fetch_earthquake_data") }}'},  # Get data from the fetching task 
    dag=dag
)


task_fetch_earthquake_data >> task_store_to_db
# airflow users  create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin
