from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_login import UserMixin, login_user, login_required, logout_user, LoginManager, current_user
import forms
from forms import LoginForm
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from config import DevelopmentConfig
from models import db, Alumnos, Preguntas, Respuestas, Maestro

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(maestro_id):
    return Maestro.query.get(int(maestro_id))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        maestro = Maestro.query.filter_by(nombre=form.username.data).first()
        if maestro and maestro.contrasenia == form.password.data:
            login_user(maestro)
            return redirect(url_for('index'))
        else:
            flash("Usuario o contraseña incorrectos", "danger")
    return render_template("login.html", form=form)

@app.route("/index")
@login_required
def index():
    return render_template("index.html")


@app.route("/crearA", methods=["GET", "POST"])
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
        # Insertar Alumnos
        db.session.add(alumno)
        db.session.commit()
        flash("Alumnos agregado correctamente", "success")
        return redirect(url_for('crearA'))
    return render_template("crear_A.html", form=create_forms)

@app.route("/crearE", methods=["GET", "POST"])
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
        # Insertar Preguntas
        db.session.add(pregunta)
        db.session.commit()
        flash("Pregunta creada", "success")
    return render_template("crear_E.html", form=create_forms)

@app.route("/resolver/<int:alumno_id>", methods=["GET", "POST"])
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
        
        flash(f"Examen completado. Calificación: {calificacion}", "success")
        return redirect(url_for('calif'))
    
    return render_template("resolver.html", preguntas=preguntas, alumno=alumno, edad=edad)

@app.route("/calif")
def calif():
    grupos = db.session.query(Alumnos.grupo).distinct().all()
    alumnos = Alumnos.query.all()
    return render_template("calif.html", grupos=grupos, alumnos=alumnos)

@app.route("/load_group")
def load_group():
    group = request.args.get('group')
    filtered_alumnos = Alumnos.query.filter_by(grupo=group).all()
    alumnos_data = [{'nombre': alum.nombre, 'apaterno': alum.apaterno, 'amaterno': alum.amaterno, 'grupo': alum.grupo, 'calificacion': alum.calificacion} for alum in filtered_alumnos]
    return jsonify({'alumnos': alumnos_data})

@app.route("/buscar_A", methods=["GET", "POST"])
def buscar_A():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apaterno = request.form['apaterno'] 
        alumno = Alumnos.query.filter_by(
            nombre = nombre,
            apaterno = apaterno,
        ).first()
        
        if alumno:
            return redirect(url_for('resolver', alumno_id=alumno.id))
        else:
            flash("Alumno no encontrado", "danger")
            return redirect(url_for('buscar_A'))
    
    return render_template("buscar_A.html", )

if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)