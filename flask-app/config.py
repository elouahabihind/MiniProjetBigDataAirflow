# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://username:password@localhost:3306/datawarehouse"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
