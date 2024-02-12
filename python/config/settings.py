import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

FLASK_SERVER_PORT = os.environ.get('FLASK_SERVER_PORT', 5000)
DEBUG = os.environ.get('DEBUG', False)

TRUELINK_SFTP_HOST = os.environ['TRUELINK_SFTP_HOST']
TRUELINK_SFTP_USER = os.environ['TRUELINK_SFTP_USER']
TRUELINK_SSH_KEY_BASE64 = os.environ['TRUELINK_SSH_KEY_BASE64']

CLIMATE_DB_USER = os.environ['CLIMATE_DB_USER']
CLIMATE_DB_PASS = os.environ['CLIMATE_DB_PASS']
CLIMATE_DB_HOST = os.environ['CLIMATE_DB_HOST']
CLIMATE_DB_PORT = os.environ['CLIMATE_DB_PORT']
CLIMATE_DB_DATABASE = os.environ['CLIMATE_DB_DATABASE']

CUSTOM_DATA_CONNECTOR_HOST = os.environ['CUSTOM_DATA_CONNECTOR_HOST']

class Routes(Enum):
    CLIMATE_DB = 1
    BI_SYS = 2

class Types(Enum):
    FUEL = {'keyword': 'Brændstof', 'route': Routes.CLIMATE_DB, 'prefix': 'truelink'}
    ECOMM = {'keyword': 'E-handelsfilter', 'route': Routes.BI_SYS, 'prefix': 'ØK'}