from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.secret_key = 'contraseña'

# Configuración de la base de datos MongoDB con MongoEngine
app.config['MONGODB_SETTINGS'] = {
    'db': 'GESTIONPRODUCTOS1',
    'host': 'mongodb://localhost:27017/GESTIONPRODUCTOS1'
}
db = MongoEngine(app)

from controller.productoC import *
from controller.usuarioC import *

# Definimos el modelo de datos de Usuario


if __name__ == "__main__":
    app.run(port=3000, debug=True)
    