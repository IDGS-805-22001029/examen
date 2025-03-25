from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Maestro
import logging

maestros_bp = Blueprint('maestros', __name__, template_folder='../templates/maestros')

@maestros_bp.route('/maestros', methods=['GET', 'POST'])
@login_required
def maestros():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contrasenia = request.form['contrasenia']
        maestro = Maestro(nombre=nombre, contrasenia=contrasenia)
        db.session.add(maestro)
        db.session.commit()
        logging.info(f"Usuario {current_user.nombre} agregó un maestro: {nombre}.")
        flash("Maestro agregado correctamente", "success")
        return redirect(url_for('maestros.maestros'))
    maestros = Maestro.query.all()
    return render_template('maestros/index.html', maestros=maestros)