# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DimRegion(db.Model):
    __tablename__ = 'dim_region'
    region_id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(50), unique=True)

class DimCountry(db.Model):
    __tablename__ = 'dim_country'
    country_id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(50), unique=True)

class DimCity(db.Model):
    __tablename__ = 'dim_city'
    city_id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), unique=True)

class DimMonth(db.Model):
    __tablename__ = 'dim_month'
    month_id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, unique=True)

class DimDay(db.Model):
    __tablename__ = 'dim_day'
    day_id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, unique=True)

class DimYear(db.Model):
    __tablename__ = 'dim_year'
    year_id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, unique=True)

class FactTemp(db.Model):
    __tablename__ = 'fact_temp'
    temp_id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, db.ForeignKey('dim_region.region_id'))
    country_id = db.Column(db.Integer, db.ForeignKey('dim_country.country_id'))
    city_id = db.Column(db.Integer, db.ForeignKey('dim_city.city_id'))
    month_id = db.Column(db.Integer, db.ForeignKey('dim_month.month_id'))
    day_id = db.Column(db.Integer, db.ForeignKey('dim_day.day_id'))
    year_id = db.Column(db.Integer, db.ForeignKey('dim_year.year_id'))
    temperature = db.Column(db.Numeric(5, 2))

# Fact Table: FactHumidity
class FactHumidity(db.Model):
    __tablename__ = 'fact_humidity'
    humidity_id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, db.ForeignKey('dim_region.region_id'))
    country_id = db.Column(db.Integer, db.ForeignKey('dim_country.country_id'))
    city_id = db.Column(db.Integer, db.ForeignKey('dim_city.city_id'))
    month_id = db.Column(db.Integer, db.ForeignKey('dim_month.month_id'))
    day_id = db.Column(db.Integer, db.ForeignKey('dim_day.day_id'))
    year_id = db.Column(db.Integer, db.ForeignKey('dim_year.year_id'))
    humidity = db.Column(db.Numeric(5, 2))

# Fact Table: FactPressure
class FactPressure(db.Model):
    __tablename__ = 'fact_pressure'
    pressure_id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, db.ForeignKey('dim_region.region_id'))
    country_id = db.Column(db.Integer, db.ForeignKey('dim_country.country_id'))
    city_id = db.Column(db.Integer, db.ForeignKey('dim_city.city_id'))
    month_id = db.Column(db.Integer, db.ForeignKey('dim_month.month_id'))
    day_id = db.Column(db.Integer, db.ForeignKey('dim_day.day_id'))
    year_id = db.Column(db.Integer, db.ForeignKey('dim_year.year_id'))
    pressure = db.Column(db.Numeric(7, 2))

# Fact Table: FactWind
class FactWind(db.Model):
    __tablename__ = 'fact_wind'
    wind_id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, db.ForeignKey('dim_region.region_id'))
    country_id = db.Column(db.Integer, db.ForeignKey('dim_country.country_id'))
    city_id = db.Column(db.Integer, db.ForeignKey('dim_city.city_id'))
    month_id = db.Column(db.Integer, db.ForeignKey('dim_month.month_id'))
    day_id = db.Column(db.Integer, db.ForeignKey('dim_day.day_id'))
    year_id = db.Column(db.Integer, db.ForeignKey('dim_year.year_id'))
    wind_speed = db.Column(db.Numeric(5, 2))