# from dotenv import load_dotenv
# load_dotenv()
import os

basedir = os.path.abspath(os.path.dirname(__file__))

__version__ = "0.1.0"

class Config(object):
    DEBUG = os.getenv("DEBUG",False)
    CSRF_ENABLED = True
    SECRET_KEY = '57e19ea558d4967a552d0d3deece34a70'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APPINSIGHTS_CONNSTR = os.getenv("APPINSIGHTS_CONNSTR")
    ROLE = "Aka Api"
    HOST_TYPE = os.getenv("HOST_TYPE","")
    ENV = os.getenv("ENV","")
    APP_TITLE = 'AKA URL Shortner API'