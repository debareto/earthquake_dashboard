import psycopg2
import pandas as pd


def get_earthquake_data(date):
    conn = psycopg2.connect("dbname=earthquake_db user=postgres password=Debare2001 host=localhost")
    cursor = conn.cursor()

    query = """
        SELECT latitude, longitude, magnitude, location, time
        FROM earthquakes
        WHERE DATE(time) = %s;
    """
    cursor.execute(query, (date,))
    data = cursor.fetchall()
    cursor.close()

    df = pd.DataFrame(data, columns=['latitude', 'longitude', 'magnitude', 'location', 'time'])
    df['latitude'] = df['latitude'].astype(float)
    df['longitude'] = df['longitude'].astype(float)
    df['magnitude'] = df['magnitude'].astype(float)

    return df

