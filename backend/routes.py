from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
try:
    from .models import db, Usuario, Turno
except ImportError:
    from models import db, Usuario, Turno

routes = Blueprint('routes', __name__)

@routes.route('/api/turnos', methods=['GET'])
def obtener_turnos():
    turnos = Turno.query.all()
    turnos_json = [
        {
            'id': t.id,
            'nombre': t.nombre,
            'servicio': t.servicio,
            'fecha': t.fecha,
            'hora': t.hora,
            'correo': t.correo
        } for t in turnos
    ]
    return jsonify({'turnos': turnos_json})

def generar_horarios():
    horarios = []
    hora = 8
    minuto = 0
    while True:
        horarios.append(f"{hora:02d}:{minuto:02d}")
        minuto += 30
        if minuto == 60:
            minuto = 0
            hora += 1
        # Último turno permitido: 21:30
        if hora == 21 and minuto == 30:
            horarios.append(f"{hora:02d}:{minuto:02d}")
            break
        if hora > 21 or (hora == 21 and minuto > 30):
            break
    return horarios

routes = Blueprint('routes', __name__)

@routes.route('/api/turnos', methods=['GET'])
def obtener_turnos():
    turnos = Turno.query.all()
    turnos_json = [
        {
            'id': t.id,
            'nombre': t.nombre,
            'servicio': t.servicio,
            'fecha': t.fecha,
            'hora': t.hora,
            'correo': t.correo
        } for t in turnos
    ]
    return jsonify({'turnos': turnos_json})


@routes.route('/disponibilidad/<fecha>', methods=['GET'])
def obtener_disponibilidad(fecha):
    horarios_ocupados = [turno.hora for turno in Turno.query.filter_by(fecha=fecha).all()]
    horarios_disponibles = [hora for hora in generar_horarios() if hora not in horarios_ocupados]
    return jsonify({'disponibles': horarios_disponibles})

@routes.route('/agendar', methods=['POST'])
def agendar_turno():
    data = request.get_json()
    nuevo_turno = Turno(
        nombre=data['nombre'],
        servicio=data['servicio'],
        fecha=data['fecha'],
        hora=data['hora'],
        correo=data['correo']
    )
    db.session.add(nuevo_turno)
    db.session.commit()
    enviar_correo_confirmacion(data['correo'], data['nombre'], data['servicio'], data['fecha'], data['hora'])
    return {"mensaje": "Turno agendado con éxito"}, 201

def enviar_correo_confirmacion(correo, nombre, servicio, fecha, hora):
    from flask import current_app
    mail = current_app.extensions['mail']
    mensaje_cliente = Message(
        subject='Confirmación de Turno Agendado',
        recipients=[correo],
        body=f"Hola {nombre},\n\nTu turno para '{servicio}' ha sido agendado.\nFecha: {fecha}\nHora: {hora}\n\n¡Gracias por confiar en nosotros!"
    )
    mensaje_admin = Message(
        subject=f"Nuevo Turno Agendado: {servicio}",
        recipients=['cuentagestion001@gmail.com'],
        body=f"Se ha agendado un nuevo turno:\n\nCliente: {nombre}\nServicio: {servicio}\nFecha: {fecha}\nHora: {hora}"
    )
    mail.send(mensaje_cliente)
    mail.send(mensaje_admin)

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usuario = Usuario.query.filter_by(username=username).first()
        if usuario and usuario.check_password(password):
            login_user(usuario)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('routes.admin'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')

@routes.route('/admin')
@login_required
def admin():
    turnos = Turno.query.all()
    return render_template('admin.html', turnos=turnos)

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('routes.login'))

@routes.route('/eliminar_turno/<int:id>', methods=['POST'])
@login_required
def eliminar_turno(id):
    turno = Turno.query.get(id)
    if turno:
        db.session.delete(turno)
        db.session.commit()
        flash('Turno eliminado', 'success')
    return redirect(url_for('routes.admin'))
