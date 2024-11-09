import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.mysql_hook import MySqlHook
from datetime import datetime, timedelta

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 11, 1),  # Adjust start date
}

API_KEY = "c6e808e073d4c8cfa219679c148ad912"
API_BASE_URL = "http://api.weatherstack.com/current?access_key={}&query={}"

# Read the city list from file and return as a list of dictionaries
def read_city_file(file_path='/home/mohcine/cities.txt'):
    cities = []
    with open(file_path, 'r') as file:
        for line in file:
            city, region, country = line.strip().split(',')
            cities.append({
                'city': city,
                'region': region,
                'country': country
            })
    return cities

# Fetch weather data from the API for a given city
def fetch_weather_data(city_info):
    response = requests.get(API_BASE_URL.format(API_KEY, city_info['city']))
    data = response.json()
    return data if response.status_code == 200 and "current" in data else None

# Insert into dimension tables and get or insert IDs
def get_or_insert_dim_id(hook, table_name, column_name, value):
    sql_check = f"SELECT {column_name}_id FROM {table_name} WHERE {column_name} = %s"
    result = hook.get_first(sql_check, parameters=(value,))
    if result:
        return result[0]

    sql_insert = f"INSERT INTO {table_name} ({column_name}) VALUES (%s)"
    hook.run(sql_insert, parameters=(value,))
    return hook.get_first(sql_check, parameters=(value,))[0]

# Transform and load the data into the warehouse
def transform_and_load_to_datawarehouse():
    cities = read_city_file()  # Read cities from file
    warehouse_hook = MySqlHook(mysql_conn_id='datawarehouse')

    for city_info in cities:
        data = fetch_weather_data(city_info)
        if not data:
            print(f"Could not fetch data for {city_info['city']}")
            continue

        # Extract data from response
        temperature = data['current']['temperature']
        pressure = data['current']['pressure']
        humidity = data['current']['humidity']
        wind_speed = data['current']['wind_speed']
        timestamp = datetime.utcfromtimestamp(data['location']['localtime_epoch'])

        # Retrieve or insert dimension IDs
        city_id = get_or_insert_dim_id(warehouse_hook, 'dim_city', 'city', city_info['city'])
        region_id = get_or_insert_dim_id(warehouse_hook, 'dim_region', 'region', city_info['region'])
        country_id = get_or_insert_dim_id(warehouse_hook, 'dim_country', 'country', city_info['country'])
        day_id = get_or_insert_dim_id(warehouse_hook, 'dim_day', 'day', timestamp.day)
        month_id = get_or_insert_dim_id(warehouse_hook, 'dim_month', 'month', timestamp.month)
        year_id = get_or_insert_dim_id(warehouse_hook, 'dim_year', 'year', timestamp.year)

        # Insert data into fact tables
        try:
            # Insert into fact_pressure
            sql_pressure = """
            INSERT INTO fact_pressure (city_id, region_id, country_id, day_id, month_id, year_id, pressure)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            warehouse_hook.run(sql_pressure, parameters=(city_id, region_id, country_id, day_id, month_id, year_id, pressure))

            # Insert into fact_humidity
            sql_humidity = """
            INSERT INTO fact_humidity (city_id, region_id, country_id, day_id, month_id, year_id, humidity)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            warehouse_hook.run(sql_humidity, parameters=(city_id, region_id, country_id, day_id, month_id, year_id, humidity))

            # Insert into fact_wind
            sql_wind = """
            INSERT INTO fact_wind (city_id, region_id, country_id, day_id, month_id, year_id, wind_speed)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            warehouse_hook.run(sql_wind, parameters=(city_id, region_id, country_id, day_id, month_id, year_id, wind_speed))

            print(f"Data inserted for {city_info['city']}")

        except Exception as e:
            print(f"Error inserting data for {city_info['city']}: {e}")

# Define the DAG with a daily schedule
with DAG(
    'weather_data_etl_from_api',
    default_args=default_args,
    description='ETL pipeline for weather data from API to MySQL data warehouse',
    schedule_interval='@daily',  # Set to run daily
    catchup=False,
) as dag:

    load_data_task = PythonOperator(
        task_id='transform_and_load_to_datawarehouse',
        python_callable=transform_and_load_to_datawarehouse,
    )

    load_data_task
