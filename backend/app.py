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

# Configuración de correo electrónico
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'cuentagestion001@gmail.com'
app.config['MAIL_PASSWORD'] = 'bzij rqbk lmjp pgry'
app.config['MAIL_DEFAULT_SENDER'] = 'cuentagestion001@gmail.com'

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
