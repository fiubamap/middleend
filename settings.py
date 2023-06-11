import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

GEOSERVER_BASE_URL = os.environ.get('GEOSERVER_BASE_URL')
GEOSERVER_WPS_URL = os.environ.get('GEOSERVER_WPS_URL')
GEOSERVER_USERNAME = os.environ.get('GEOSERVER_USERNAME')
GEOSERVER_PASSWORD = os.environ.get('GEOSERVER_PASSWORD')
