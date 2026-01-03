import os
from dotenv import load_dotenv

# Cargamos el archivo .env
load_dotenv()

# Leemos las variables. Si no existen, os.getenv devuelve None
API_URL = os.getenv("API_URL")
API_EMAIL = os.getenv("API_EMAIL")
API_KEY = os.getenv("API_KEY")
API_TYPE = os.getenv("API_TYPE")
API_ROWS = os.getenv("API_ROWS")

# Validación simple: Si falta algo, avisamos y paramos el programa
if not API_KEY or not API_EMAIL:
    raise ValueError("¡Faltan variables en el archivo .env! Revisa API_KEY y API_EMAIL")