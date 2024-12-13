import requests
import psycopg2
from datetime import datetime
import os





def fetch_and_store_earthquake_data(start_date, end_date):

    # Fetch the password from environment variables
    db_password = os.getenv("DB_PASSWORD")
        
    # Connect to PostgreSQL
    conn = psycopg2.connect(f"dbname=earthquake_db user=postgres password={db_password} host=localhost")
    cursor = conn.cursor()
    print('connection to the db established')


    API_URL  = "https://earthquake.usgs.gov/fdsnws/event/1/query"

    params = {
        "format": "geojson",
        "starttime": start_date,
        "endtime": end_date,
    }
    response = requests.get(API_URL, params=params)
    data = response.json()

    for feature in data['features']:
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
    print(f'Earthquake data between {start_date} and {end_date} saved in the earthquake table')

    cursor.close()
    conn.close()
    print('connection to the db closed')


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


fetch_data(start_date="2024-12-08", end_date="2024-12-09")

# fetch_and_store_earthquake_data(start_date="2024-01-01", end_date="2024-01-30")

