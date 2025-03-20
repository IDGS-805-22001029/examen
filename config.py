import os
from sqlalchemy import create_engine
import urllib 

class Config(object):
    SECRET_KEY = 'mysecretkey'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/examen'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    