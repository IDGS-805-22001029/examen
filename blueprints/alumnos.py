from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Alumnos, Preguntas, Respuestas
from datetime import datetime
import forms
import logging

alumnos_bp = Blueprint('alumnos', __name__, template_folder='../templates')

@alumnos_bp.route("/crearA", methods=["GET", "POST"])
@login_required
def crearA():
    create_forms = forms.AlumnoForm(request.form)
    if request.method == 'POST':
        alumno = Alumnos(
            nombre=create_forms.nombre.data,
            apaterno=create_forms.apaterno.data,
            amaterno=create_forms.amaterno.data,
            fecha_nacimiento=create_forms.fecha_nacimiento.data,
            grupo=create_forms.grupo.data
        )
        db.session.add(alumno)
        db.session.commit()
        logging.info(f"Usuario {current_user.nombre} agregó un alumno: {alumno.nombre} {alumno.apaterno}.")
        flash("Alumno agregado correctamente", "success")
        return redirect(url_for('alumnos.crearA'))
    return render_template("crear_A.html", form=create_forms)

@alumnos_bp.route("/calif")
@login_required
def calif():
    grupos = db.session.query(Alumnos.grupo).distinct().all()
    alumnos = Alumnos.query.all()
    logging.info(f"Usuario {current_user.nombre} accedió a la página de calificaciones.")
    return render_template("calif.html", grupos=grupos, alumnos=alumnos)

@alumnos_bp.route("/load_group")
@login_required
def load_group():
    group = request.args.get('group')
    filtered_alumnos = Alumnos.query.filter_by(grupo=group).all()
    alumnos_data = [{'nombre': alum.nombre, 'apaterno': alum.apaterno, 'amaterno': alum.amaterno, 'grupo': alum.grupo, 'calificacion': alum.calificacion} for alum in filtered_alumnos]
    logging.info(f"Usuario {current_user.nombre} cargó el grupo {group}.")
    return jsonify({'alumnos': alumnos_data})

@alumnos_bp.route("/buscar_A", methods=["GET", "POST"])
@login_required
def buscar_A():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apaterno = request.form['apaterno']
        alumno = Alumnos.query.filter_by(
            nombre=nombre,
            apaterno=apaterno,
        ).first()
        
        if alumno:
            logging.info(f"Usuario {current_user.nombre} buscó al alumno {nombre} {apaterno}.")
            return redirect(url_for('alumnos.resolver', alumno_id=alumno.id))
        else:
            logging.warning(f"Usuario {current_user.nombre} intentó buscar un alumno no encontrado: {nombre} {apaterno}.")
            flash("Alumno no encontrado", "danger")
            return redirect(url_for('alumnos.buscar_A'))
    return render_template("buscar_A.html")

@alumnos_bp.route("/resolver/<int:alumno_id>", methods=["GET", "POST"])
@login_required
def resolver(alumno_id):
    preguntas = Preguntas.query.all()
    alumno = Alumnos.query.get(alumno_id)
    
    # Convertir la fecha de nacimiento de string a datetime
    fecha_nacimiento = datetime.strptime(alumno.fecha_nacimiento, '%d/%m/%Y')
    hoy = datetime.today()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    
    if request.method == 'POST':
        respuestas_correctas = 0
        total_preguntas = len(preguntas)
        
        for pregunta in preguntas:
            respuesta_seleccionada = request.form.get(f'respuesta_{pregunta.id}')
            if respuesta_seleccionada:
                respuesta = Respuestas(
                    alumno_id=alumno.id,
                    pregunta_id=pregunta.id,
                    respuesta=respuesta_seleccionada
                )
                db.session.add(respuesta)
                if respuesta_seleccionada == pregunta.respuesta_correcta:
                    respuestas_correctas += 1
        
        calificacion = (respuestas_correctas / total_preguntas) * 100
        alumno.calificacion = calificacion
        db.session.commit()
        
        logging.info(f"Usuario {current_user.nombre} resolvió el examen del alumno {alumno.nombre}. Calificación: {calificacion}.")
        flash(f"Examen completado. Calificación: {calificacion}", "success")
        return redirect(url_for('alumnos.calif'))
    
    return render_template("resolver.html", preguntas=preguntas, alumno=alumno, edad=edad)