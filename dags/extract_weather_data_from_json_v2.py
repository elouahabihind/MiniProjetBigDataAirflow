from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.mysql_hook import MySqlHook
from datetime import datetime, timedelta
import json

# Define default arguments for the DAG
default_args = {
    'owner': 'mohcine',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Utility function to get or create dimension IDs
def get_or_create_dimension_id(hook, table_name, column_name, value):
    """Check if the value exists in the dimension table and return the ID, or create it if it doesn't exist."""
    try:
        id_column = f"{column_name}_id"
        sql_check = f"SELECT {id_column} FROM {table_name} WHERE {column_name} = %s"
        result = hook.get_first(sql_check, parameters=(value,))
        
        if result is None:
            sql_insert = f"INSERT INTO {table_name} ({column_name}) VALUES (%s)"
            hook.run(sql_insert, parameters=(value,))
            result = hook.get_first("SELECT LAST_INSERT_ID()")
        
        return result[0] if result else None
    except Exception as e:
        print(f"Error in get_or_create_dimension_id for {value} in {table_name}: {e}")
        return None

# Main ETL function
def transform_and_load_to_datawarehouse():
    json_file_path = "/home/mohcine/31_10_2024_14_00_openweathermap_weather_cities.json"

    with open(json_file_path, 'r') as file:
        weather_data = json.load(file)

    warehouse_hook = MySqlHook(mysql_conn_id='datawarehouse')

    for city, data in weather_data.items():
        try:
            temperature = data['main']['temp']
            pressure = data['main']['pressure']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            region = data.get('region')
            country = data.get('country')
            timestamp = data['dt']
            
            date = datetime.fromtimestamp(timestamp)
            day = date.day
            month = date.month
            year = date.year

            day_id = get_or_create_dimension_id(warehouse_hook, 'dim_day', 'day', day)
            month_id = get_or_create_dimension_id(warehouse_hook, 'dim_month', 'month', month)
            year_id = get_or_create_dimension_id(warehouse_hook, 'dim_year', 'year', year)
            city_id = get_or_create_dimension_id(warehouse_hook, 'dim_city', 'city', city)
            region_id = get_or_create_dimension_id(warehouse_hook, 'dim_region', 'region', region)
            country_id = get_or_create_dimension_id(warehouse_hook, 'dim_country', 'country', country)

            if not all([city_id, region_id, country_id, day_id, month_id, year_id]):
                print(f"Skipping data for {city} due to missing dimension IDs.")
                continue

            try:
                sql_pressure = """
                INSERT INTO fact_pressure (city_id, region_id, country_id, day_id, month_id, year_id, pressure)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                warehouse_hook.run(sql_pressure, parameters=(city_id, region_id, country_id, day_id, month_id, year_id, pressure))
                print(f"Inserted into fact_pressure for {city}: {pressure}")
            except Exception as e:
                print(f"Error inserting into fact_pressure for {city}: {e}")

            try:
                sql_humidity = """
                INSERT INTO fact_humidity (city_id, region_id, country_id, day_id, month_id, year_id, humidity)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                warehouse_hook.run(sql_humidity, parameters=(city_id, region_id, country_id, day_id, month_id, year_id, humidity))
                print(f"Inserted into fact_humidity for {city}: {humidity}")
            except Exception as e:
                print(f"Error inserting into fact_humidity for {city}: {e}")

            try:
                sql_wind = """
                INSERT INTO fact_wind (city_id, region_id, country_id, day_id, month_id, year_id, wind_speed)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                warehouse_hook.run(sql_wind, parameters=(city_id, region_id, country_id, day_id, month_id, year_id, wind_speed))
                print(f"Inserted into fact_wind for {city}: {wind_speed}")
            except Exception as e:
                print(f"Error inserting into fact_wind for {city}: {e}")

        except Exception as e:
            print(f"Error processing city {city}: {e}")

# Define the DAG with a unique name
with DAG(
    'weather_data_etl_from_json_file_v2',
    default_args=default_args,
    description='ETL pipeline for weather data to MySQL data warehouse',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 11, 1),
    catchup=False,
) as dag:

    # Define task to load data into the warehouse
    load_data_task = PythonOperator(
        task_id='transform_and_load_to_datawarehouse',
        python_callable=transform_and_load_to_datawarehouse,
    )

    load_data_task
