from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Alumnos
import logging

alumnos_bp = Blueprint('alumnos', __name__, template_folder='../templates/alumnos')

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
        logging.info(f"Usuario {current_user.nombre} agregó un alumno: {nombre} {apaterno}.")
        flash("Alumno agregado correctamente", "success")
        return redirect(url_for('alumnos.alumnos'))
    alumnos = Alumnos.query.all()
    return render_template('alumnos/index.html', alumnos=alumnos)