from flask import Flask, url_for
from companyview.helpers.forms import SignupForm
from config import Config
from .database.user_db import reset_table
from flask_login import current_user, LoginManager
from .routes import global_scope, api_scope, errors_scope
import sqlite3
from .database import user_db
import os
from dotenv import load_dotenv  # Instalar con pip install python-dotenv

load_dotenv()  # Carga todo el contenido de .env en variables de entorno


# agrego lo necesario para el log in

app = Flask(
    __name__, static_folder=Config.STATIC_FOLDER, template_folder=Config.TEMPLATE_FOLDER
)
app.config.from_object(Config)

app.config[
    "SECRET_KEY"
] = os.getenv("SECRET_KEY","")
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return user_db.get_by_id(int(user_id))


app.register_blueprint(global_scope, url_prefix="/")
app.register_blueprint(errors_scope, url_prefix="/")
app.register_blueprint(api_scope, url_prefix="/api")

# reset_table() # Borrar al terminar testeo


"""
connection = sqlite3.connect('companyview/database/database.db')


with open('companyview/database/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()


connection.commit()
connection.close()



print("--------------------------------", current_user)
"""