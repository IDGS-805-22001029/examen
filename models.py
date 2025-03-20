from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime

db=SQLAlchemy()
class Alumnos(db.Model):
    __tablename__='alumno'
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(50))
    apaterno=db.Column(db.String(50))
    amaterno=db.Column(db.String(50))
    fecha_nacimiento=db.Column(db.String(10))
    grupo= db.Column(db.String(10))
    calificacion=db.Column(db.Float)

class Maestro(db.Model,UserMixin):
    __tablename__='maestro'
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(50))
    contrasenia=db.Column(db.String(50))

class Preguntas(db.Model):
    __tablename__='pregunta'
    id=db.Column(db.Integer, primary_key=True)
    pregunta=db.Column(db.String(100))
    respuesta_a=db.Column(db.String(100))
    respuesta_b=db.Column(db.String(100))
    respuesta_c=db.Column(db.String(100))
    respuesta_d=db.Column(db.String(100))
    respuesta_correcta=db.Column(db.String(12))


class Respuestas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'), nullable=False)
    pregunta_id = db.Column(db.Integer, db.ForeignKey('pregunta.id'), nullable=False)
    respuesta = db.Column(db.String(1), nullable=False)