# app.py
from flask import Flask, render_template, jsonify
from config import Config
from models import db, FactTemp, DimCity, DimRegion, DimCountry, DimYear, DimMonth, DimDay,FactHumidity,FactPressure,FactWind

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/temperature')
def temperature():
    data = db.session.query(FactTemp, DimCity, DimRegion, DimCountry, DimYear, DimMonth, DimDay)\
        .join(DimCity, FactTemp.city_id == DimCity.city_id)\
        .join(DimRegion, FactTemp.region_id == DimRegion.region_id)\
        .join(DimCountry, FactTemp.country_id == DimCountry.country_id)\
        .join(DimYear, FactTemp.year_id == DimYear.year_id)\
        .join(DimMonth, FactTemp.month_id == DimMonth.month_id)\
        .join(DimDay, FactTemp.day_id == DimDay.day_id).all()
    
    result = [
        {
            'date': f"{item.DimYear.year}-{item.DimMonth.month}-{item.DimDay.day}",
            'temperature': item.FactTemp.temperature,
            'city': item.DimCity.city,
            'region': item.DimRegion.region,
            'country': item.DimCountry.country
        }
        for item in data
    ]
    return jsonify(result)

@app.route('/humidity')
def humidity():
    data = db.session.query(FactHumidity, DimCity, DimRegion, DimCountry, DimYear, DimMonth, DimDay)\
        .join(DimCity, FactHumidity.city_id == DimCity.city_id)\
        .join(DimRegion, FactHumidity.region_id == DimRegion.region_id)\
        .join(DimCountry, FactHumidity.country_id == DimCountry.country_id)\
        .join(DimYear, FactHumidity.year_id == DimYear.year_id)\
        .join(DimMonth, FactHumidity.month_id == DimMonth.month_id)\
        .join(DimDay, FactHumidity.day_id == DimDay.day_id).all()
    
    result = [
        {
            'date': f"{item.DimYear.year}-{item.DimMonth.month}-{item.DimDay.day}",
            'humidity': item.FactHumidity.humidity,
            'city': item.DimCity.city,
            'region': item.DimRegion.region,
            'country': item.DimCountry.country
        }
        for item in data
    ]
    return jsonify(result)

@app.route('/pressure')
def pressure():
    data = db.session.query(FactPressure, DimCity, DimRegion, DimCountry, DimYear, DimMonth, DimDay)\
        .join(DimCity, FactPressure.city_id == DimCity.city_id)\
        .join(DimRegion, FactPressure.region_id == DimRegion.region_id)\
        .join(DimCountry, FactPressure.country_id == DimCountry.country_id)\
        .join(DimYear, FactPressure.year_id == DimYear.year_id)\
        .join(DimMonth, FactPressure.month_id == DimMonth.month_id)\
        .join(DimDay, FactPressure.day_id == DimDay.day_id).all()
    
    result = [
        {
            'date': f"{item.DimYear.year}-{item.DimMonth.month}-{item.DimDay.day}",
            'pressure': item.FactPressure.pressure,
            'city': item.DimCity.city,
            'region': item.DimRegion.region,
            'country': item.DimCountry.country
        }
        for item in data
    ]
    return jsonify(result)

@app.route('/wind')
def wind():
    data = db.session.query(FactWind, DimCity, DimRegion, DimCountry, DimYear, DimMonth, DimDay)\
        .join(DimCity, FactWind.city_id == DimCity.city_id)\
        .join(DimRegion, FactWind.region_id == DimRegion.region_id)\
        .join(DimCountry, FactWind.country_id == DimCountry.country_id)\
        .join(DimYear, FactWind.year_id == DimYear.year_id)\
        .join(DimMonth, FactWind.month_id == DimMonth.month_id)\
        .join(DimDay, FactWind.day_id == DimDay.day_id).all()
    
    result = [
        {
            'date': f"{item.DimYear.year}-{item.DimMonth.month}-{item.DimDay.day}",
            'wind_speed': item.FactWind.wind_speed,
            'city': item.DimCity.city,
            'region': item.DimRegion.region,
            'country': item.DimCountry.country
        }
        for item in data
    ]
    return jsonify(result)


@app.route('/temperature_data')
def temperature_data():
    return render_template('temperature.html')

@app.route('/pressure_data')
def pressure_data():
    return render_template('pressure.html')

@app.route('/wind_data')
def wind_data():
    return render_template('wind.html')

@app.route('/humidity_data')
def humidity_data():
    return render_template('humidity.html')

if __name__ == '__main__':
    app.run(debug=True)
