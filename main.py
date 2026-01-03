import logging
from urllib3.util import Retry
from requests import Session
from requests.adapters import HTTPAdapter
import config
import requests
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa

# 1. Configuración del Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_session():
    s = Session()
    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods={'GET'},
    )
    s.mount('https://', HTTPAdapter(max_retries=retries))
    return s

def transform_data(data):
    df = pd.DataFrame(data['tables']['orders'])

    # Verifico si la tabla no está vacía
    if df.isnull().all().all():
        logger.warning("El DataFrame está vacío o todos los valores son nulos.")

    # Convierto order_date a datetime
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

    # Agrego las columnas de año y mes
    df['year'] = df['order_date'].dt.year
    df['month'] = df['order_date'].dt.month

    return df

def load_data(df):
    # Guardamos el DataFrame en formato Parquet, particionado por año y mes
    df.to_parquet(
        path='output/orders',
        engine='pyarrow',
        partition_cols=['year', 'month'],
    )
    logger.info("Datos guardados en formato Parquet con particiones")

if __name__ == "__main__":
    session = get_session()
    logger.info(f"Conectando a {config.API_URL}...")

    try:
        response = session.get(
            config.API_URL, 
            params={'email': config.API_EMAIL, 'key': config.API_KEY, 'type': config.API_TYPE, 'rows': config.API_ROWS, 'timeout': 10},
        )
        response.raise_for_status() 
        
        data = response.json()
        logger.info("¡Datos descargados con éxito!")
        
        df_cleaned = transform_data(data)
        load_data(df_cleaned)
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error crítico después de reintentos: {e}")