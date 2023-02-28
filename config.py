import os
from dotenv import load_dotenv  # Instalar con pip install python-dotenv

load_dotenv()  # Carga todo el contenido de .env en variables de entorno


class Config:
    DEBUG = False

    DATABASE_PATH = "companyview/database/database.db"
    DB_TOKEN = os.environ.get("DB_TOKEN", "")  # Para Encriptar la DB
    ENCRYPT_DB = True

    TEMPLATE_FOLDER = "views/templates/"
    STATIC_FOLDER = "views/static/"
