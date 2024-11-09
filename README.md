# Mini Project: Data Pipeline with Apache Airflow

## Created by:
- Hind El Ouahabi
- Mohcine Boudenjal

Supervised by:  
- Yasyn El Yusufi

## Project Description

This project implements a complete data pipeline for the ingestion, transformation, and loading of weather data from various sources. Using Apache Airflow, the data is orchestrated to be collected, structured, and loaded into a MySQL data warehouse, enabling analysis and visualization through a web application built with Flask and Chart.js.

## Project Architecture

The general architecture of our project is based on several interconnected components, including Apache Airflow for orchestrating workflows, MySQL for data storage, and Flask for data visualization.

### Architecture Diagram
![Project Architecture](/img/architechture.png)

## Conception

For data warehousing, we designed star schemas to centralize weather metrics, such as temperature, humidity, pressure, and wind, which are linked to relevant dimensions (city, region, country, month, day, year).

### Example Schemas:
![Fact Table Schema - Temperature](/img/fact_temperature.png)

## How to Run the Project

### Step 1: Initialize Data

1. **Import Database Schemas**  
   - Import the weather database schema:
     ```bash
     mysql -u [username] -p weather < weather_schema.sql
     ```
   - Import the data warehouse schema:
     ```bash
     mysql -u [username] -p datawarehouse < datawarehouse_schema.sql
     ```

2. **Save JSON Weather Data**  
   Download and save the JSON file from OpenWeatherMap and store it in the appropriate directory for data ingestion.

3. **Launch Apache Airflow**  
   - Start the Airflow web server:
     ```bash
     airflow webserver --port 8080
     ```
   - Start the scheduler:
     ```bash
     airflow scheduler
     ```

4. **Create Database Connection in Airflow**  
   - In the Airflow UI, create a MySQL connection named `mysqlconn` pointing to your MySQL data warehouse.

5. **Save DAGs and Activate**  
   Save your DAG files in the Airflow DAGs directory, activate them, and trigger the DAGs for data ingestion and transformation.

### Step 2: Launch Flask Application

1. **Install Dependencies**  
   Install the required Python dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```
2. **Modify config.py by adding credentials of database**  

3. **Run Application flask**  
    Install the required Python dependencies by running:
    ```bash
    flask run
    ```

## Visualisation:

The Flask web application retrieves the data from the MySQL data warehouse and visualizes it using Chart.js.

![Temperature By Month](/img/temperature.png)
![Wind Speed By Region](/img/wind.png)

## Conclusion

This project provides an end-to-end solution for ingesting, processing, and visualizing weather data. Apache Airflow orchestrates the ETL pipeline, MySQL serves as the data warehouse, and Flask offers a powerful platform for data visualization. With these technologies, the system is scalable, robust, and easy to extend with additional data sources or features.
