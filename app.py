import logging
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_required, current_user
from config import DevelopmentConfig
from models import db, Maestro, Alumnos, Preguntas, Respuestas
from blueprints.alumnos import alumnos_bp
from blueprints.maestros import maestros_bp
from blueprints.auth import auth_bp
from datetime import datetime

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app)

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(maestro_id):
    return Maestro.query.get(int(maestro_id))

app.register_blueprint(alumnos_bp)
app.register_blueprint(maestros_bp)
app.register_blueprint(auth_bp)



if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    logging.info("Aplicación iniciada.")
    app.run(debug=True)