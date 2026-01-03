# Pipeline ETL con API REST, Pandas y Parquet

Este proyecto implementa un pipeline de extracción, transformación y carga (ETL) robusto utilizando Python. Consume datos de una API pública simulada, maneja errores de red con estrategias de reintento (Backoff), transforma los datos con Pandas y los guarda en formato optimizado (Parquet) particionado por fecha.

## Características

* **Extracción Resiliente:** Implementación de `requests.Session` con `HTTPAdapter` y estrategia de `Retry` (Exponential Backoff) para manejar caídas de red o Rate Limiting.
* **Seguridad:** Gestión de credenciales mediante variables de entorno (`.env`), evitando hardcoding de secretos.
* **Logging:** Sistema de logs configurado para trazabilidad de la ejecución (INFO, WARNING, ERROR).
* **Almacenamiento Optimizado:** Los datos se guardan en formato **Parquet** usando la librería `pyarrow`, particionados por Año y Mes (`hive-partitioning`) para consultas eficientes.

## Tecnologias utilizadas

* **Python 3.10+**
* **Requests & Urllib3:** Para peticiones HTTP robustas.
* **Pandas:** Para limpieza y transformación de datos.
* **PyArrow:** Motor para escritura de archivos Parquet.
* **Python-Dotenv:** Para manejo de configuración.

## Configuración e instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/juancruzgodoy/pipeline-api-rest
    cd pipeline-api-rest
    ```

2.  **Crear entorno virtual (Opcional):**
    ```bash
    python -m venv venv
    # En Windows:
    venv\Scripts\activate
    # En Mac/Linux:
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Variables de Entorno:**
    Crea un archivo llamado `.env` en la raíz del proyecto y agrega el siguiente contenido:

    ```env
    API_URL=[https://iansaura.com/api/datasets.php](https://iansaura.com/api/datasets.php)
    API_EMAIL=email@ejemplo.com
    API_KEY=token
    API_TYPE=ecommerce
    API_ROWS=5000
    ```

## Ejecución

Para correr el pipeline completo, ejecuta el script principal:

```bash
python main.py
```

Deberías ver los logs en la consola indicando el progreso:

```text
2024-01-03 15:30:00 - INFO - Conectando a [https://iansaura.com/api/datasets.php](https://iansaura.com/api/datasets.php)...
2024-01-03 15:30:02 - INFO - ¡Datos descargados con éxito!
2024-01-03 15:30:03 - INFO - ¡Datos guardados en formato Parquet con particiones!
```

## Estructura de Salida

Los datos se guardarán automáticamente en la carpeta `output/`, organizados jerárquicamente por fecha:

```text
output/
└── orders/
    ├── year=2023/
    │   ├── month=1/
    │   │   └── data.parquet
    │   └── ...
    └── year=2024/
        ├── month=10/
        └── ...
```
