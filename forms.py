from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms import validators
from wtforms.validators import ValidationError
import re

def validate_respuesta_correcta(form, field):
    if not re.match(r'^[A-D]$', field.data):
        raise ValidationError('La respuesta correcta debe ser un solo carácter en mayúscula (A, B, C o D)')

def validate_fecha_nacimiento(form, field):
    if not re.match(r'^\d{2}/\d{2}/\d{4}$', field.data):
        raise ValidationError('La fecha de nacimiento debe estar en formato dd/mm/yyyy')

class AlumnoForm(FlaskForm):
    id = IntegerField('id', [
        validators.number_range(min=1, max=20, message='valor no valido')
    ])
    nombre = StringField('Nombre', [
        validators.DataRequired(message='El nombre es requerido'),
        validators.length(min=4, max=20, message='requiere min=4 max=20')
    ])
    apaterno = StringField('Apellido Paterno', [
        validators.DataRequired(message='El apellido es requerido')
    ])
    amaterno = StringField('Apellido Materno', [
        validators.DataRequired(message='El apellido es requerido')
    ])
    fecha_nacimiento = StringField('Fecha de Nacimiento', [
        validators.DataRequired(message='El apellido es requerido'),
        validate_fecha_nacimiento
    ])
    grupo = StringField('Grupo', [
        validators.DataRequired(message='El apellido es requerido')
    ])

class PreguntaForm(FlaskForm):
    id = IntegerField('id', [
        validators.number_range(min=1, max=20, message='valor no valido')
    ])
    pregunta = StringField('Pregunta', [
        validators.DataRequired(message='La pregunta es requerida')
    ])
    respuesta_a = StringField('Respuesta A', [
        validators.DataRequired(message='La respuesta es requerida')
    ])
    respuesta_b = StringField('Respuesta B', [
        validators.DataRequired(message='La respuesta es requerida')
    ])
    respuesta_c = StringField('Respuesta C', [
        validators.DataRequired(message='La respuesta es requerida')
    ])
    respuesta_d = StringField('Respuesta D', [
        validators.DataRequired(message='La respuesta es requerida')
    ])
    respuesta_correcta = StringField('Respuesta Correcta', [
        validators.DataRequired(message='La respuesta es requerida'),
        validate_respuesta_correcta
    ])

class LoginForm(FlaskForm):
    username = StringField('Username', [
        validators.DataRequired(message='El nombre de usuario es requerido')
    ])
    password = StringField('Password', [
        validators.DataRequired(message='La contraseña es requerida')
    ])

class MaestroForm(FlaskForm):
    id = IntegerField('id', [
        validators.number_range(min=1, max=20, message='valor no valido')
    ])
    nombre = StringField('Nombre', [
        validators.DataRequired(message='El nombre es requerido')
    ])
    contrasenia = StringField('Contraseña', [
        validators.DataRequired(message='La contraseña es requerida')
    ])
