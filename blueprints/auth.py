from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from forms import LoginForm
from models import Maestro, db, Alumnos
import logging

auth_bp = Blueprint('auth', __name__, template_folder='../templates')
alumnos_bp = Blueprint('alumnos', __name__, template_folder='../templates')

@auth_bp.route('/')
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        maestro = Maestro.query.filter_by(nombre=form.username.data).first()
        if maestro and maestro.contrasenia == form.password.data:
            login_user(maestro)
            logging.info(f"Usuario {maestro.nombre} inició sesión.")
            return redirect(url_for('auth.index'))
        else:
            logging.warning(f"Intento fallido de inicio de sesión para el usuario {form.username.data}.")
            flash("Usuario o contraseña incorrectos", "danger")
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        logging.info(f"Usuario {current_user.nombre} cerró sesión.")
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/index')
@login_required
def index():
    return render_template('index.html')

@alumnos_bp.route('/alumnos', methods=['GET', 'POST'])
@login_required
def alumnos():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apaterno = request.form['apaterno']
        amaterno = request.form['amaterno']
        grupo = request.form['grupo']
        alumno = Alumnos(nombre=nombre, apaterno=apaterno, amaterno=amaterno, grupo=grupo)
        db.session.add(alumno)
        db.session.commit()
        flash("Alumno agregado correctamente", "success")
        return redirect(url_for('alumnos.alumnos'))
    alumnos = Alumnos.query.all()
    return render_template('index.html', alumnos=alumnos)