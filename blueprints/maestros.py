from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Maestro, Preguntas
import forms
import logging

maestros_bp = Blueprint('maestros', __name__, template_folder='../templates')

@maestros_bp.route('/maestros', methods=['GET', 'POST'])
@login_required
def maestros():
    create_forms = forms.MaestroForm(request.form)
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
    return render_template('index_M.html', maestros=maestros, form=create_forms)

@maestros_bp.route('/maestros/eliminar/<int:id>', methods=['GET', 'POST'])
@login_required
def eliminar_maestro(id):
    maestro = Maestro.query.get_or_404(id)
    create_forms = forms.MaestroForm(request.form)
    if request.method == 'POST':
        db.session.delete(maestro)
        db.session.commit()
        logging.info(f"Usuario {current_user.nombre} eliminó al maestro: {maestro.nombre}.")
        flash("Maestro eliminado correctamente", "success")
        return redirect(url_for('maestros.maestros'))
    return render_template('index_M.html', maestro=maestro, form=create_forms)

@maestros_bp.route('/maestros/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_maestro(id):
    maestro = Maestro.query.get_or_404(id)
    create_forms = forms.MaestroForm(request.form)
    if request.method == 'POST':
        maestro.nombre = request.form['nombre']
        maestro.contrasenia = request.form['contrasenia']
        db.session.commit()
        logging.info(f"Usuario {current_user.nombre} editó al maestro: {maestro.nombre}.")
        flash("Maestro actualizado correctamente", "success")
        return redirect(url_for('maestros.maestros'))
    return render_template('editar_M.html', maestro=maestro, form=create_forms)

@maestros_bp.route("/crearE", methods=["GET", "POST"])
@login_required
def crearE():
    create_forms = forms.PreguntaForm(request.form)
    if request.method == 'POST':
        pregunta = Preguntas(
            pregunta=create_forms.pregunta.data,
            respuesta_a=create_forms.respuesta_a.data,
            respuesta_b=create_forms.respuesta_b.data,
            respuesta_c=create_forms.respuesta_c.data,
            respuesta_d=create_forms.respuesta_d.data,
            respuesta_correcta=create_forms.respuesta_correcta.data,
        )
        db.session.add(pregunta)
        db.session.commit()
        logging.info(f"Usuario {current_user.nombre} creó una pregunta: {pregunta.pregunta}.")
        flash("Pregunta creada", "success")
    return render_template("crear_E.html", form=create_forms)