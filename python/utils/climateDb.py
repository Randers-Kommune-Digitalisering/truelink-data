import sqlalchemy

from config.settings import CLIMATE_DB_USER, CLIMATE_DB_PASS, CLIMATE_DB_HOST, CLIMATE_DB_PORT, CLIMATE_DB_DATABASE

def get_connection():
    engine = sqlalchemy.create_engine(f'mariadb+mariadbconnector://{CLIMATE_DB_USER}:{CLIMATE_DB_PASS}@{CLIMATE_DB_HOST}:{CLIMATE_DB_PORT}/{CLIMATE_DB_DATABASE}')
    return engine.connect()