
import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from routes import routes
from models import db

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///turnos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'clave_secreta_segura'


# Configuración de correo electrónico usando variables de entorno
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

mail = Mail(app)
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

app.register_blueprint(routes)

@app.route('/')
def home():
    return jsonify({'mensaje': '¡Bienvenido a la API de AppTurnos!'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
