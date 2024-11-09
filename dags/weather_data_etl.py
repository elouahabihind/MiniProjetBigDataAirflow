from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.mysql_hook import MySqlHook
from datetime import datetime
import random

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 1),
}

def extract_weather_data():
    weather_hook = MySqlHook(mysql_conn_id='weather')
    
    # Execute the query to fetch random rows
    sql = "SELECT * FROM weather_data"  # Limit to 100 random rows
    records = weather_hook.get_records(sql)

    # Get column names after executing the SQL query
    with weather_hook.get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)  # Execute the SQL query
        column_names = [desc[0] for desc in cursor.description]  # Get column names
    
    # Convert rows to dictionaries with column names as keys
    weather_data_dict = [dict(zip(column_names, row)) for row in records]
    
    print("Extracted Weather Data:", weather_data_dict)  # Log the extracted data
    return weather_data_dict

def get_dimension_id(hook, table_name, column_name, value):
    sql = f"SELECT {column_name}_id FROM {table_name} WHERE {column_name} = %s"
    result = hook.get_first(sql, parameters=(value,))
    return result[0] if result else None

def insert_dimension_data(hook, table_name, column_name, value):
    sql = f"INSERT INTO {table_name} ({column_name}) VALUES (%s)"
    hook.run(sql, parameters=(value,))

def transform_and_load_to_datawarehouse(weather_data):
    warehouse_hook = MySqlHook(mysql_conn_id='datawarehouse')

    for row in weather_data:
        # Ensure required fields are present in the row
        required_fields = ['region', 'country', 'city', 'month', 'day', 'year', 'temperature']
        if not all(field in row for field in required_fields):
            print(f"Skipping row due to missing fields: {row}")
            continue  # Skip this iteration if any required field is missing

        try:
            # Insert dimensions and get IDs
            region_id = get_dimension_id(warehouse_hook, 'dim_region', 'region', row['region'])
            if not region_id:
                insert_dimension_data(warehouse_hook, 'dim_region', 'region', row['region'])
                region_id = get_dimension_id(warehouse_hook, 'dim_region', 'region', row['region'])

            country_id = get_dimension_id(warehouse_hook, 'dim_country', 'country', row['country'])
            if not country_id:
                insert_dimension_data(warehouse_hook, 'dim_country', 'country', row['country'])
                country_id = get_dimension_id(warehouse_hook, 'dim_country', 'country', row['country'])

            city_id = get_dimension_id(warehouse_hook, 'dim_city', 'city', row['city'])
            if not city_id:
                insert_dimension_data(warehouse_hook, 'dim_city', 'city', row['city'])
                city_id = get_dimension_id(warehouse_hook, 'dim_city', 'city', row['city'])

            month_id = get_dimension_id(warehouse_hook, 'dim_month', 'month', row['month'])
            if not month_id:
                insert_dimension_data(warehouse_hook, 'dim_month', 'month', row['month'])
                month_id = get_dimension_id(warehouse_hook, 'dim_month', 'month', row['month'])

            day_id = get_dimension_id(warehouse_hook, 'dim_day', 'day', row['day'])
            if not day_id:
                insert_dimension_data(warehouse_hook, 'dim_day', 'day', row['day'])
                day_id = get_dimension_id(warehouse_hook, 'dim_day', 'day', row['day'])

            year_id = get_dimension_id(warehouse_hook, 'dim_year', 'year', row['year'])
            if not year_id:
                insert_dimension_data(warehouse_hook, 'dim_year', 'year', row['year'])
                year_id = get_dimension_id(warehouse_hook, 'dim_year', 'year', row['year'])

            # Insert into fact table
            sql = """
            INSERT INTO fact_temp (region_id, country_id, city_id, month_id, day_id, year_id, temperature)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            warehouse_hook.run(sql, parameters=(
                region_id,
                country_id,
                city_id,
                month_id,
                day_id,
                year_id,
                row['temperature'],  # Temperature
            ))
        except Exception as e:
            print(f"Error processing row {row}: {e}")

# Define the DAG
dag = DAG('weather_data_etl', default_args=default_args, schedule_interval='@once')

# Define the tasks
extract_task = PythonOperator(
    task_id='extract_weather_data',
    python_callable=extract_weather_data,
    dag=dag,
)

transform_load_task = PythonOperator(
    task_id='transform_and_load_to_datawarehouse',
    python_callable=transform_and_load_to_datawarehouse,
    op_kwargs={'weather_data': extract_task.output},  # Pass extracted data to next task
    dag=dag,
)

# Set task dependencies
extract_task >> transform_load_task
