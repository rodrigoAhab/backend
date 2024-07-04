import bcrypt
from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from model.usuario import Usuario
from model.codigos_unicos import Codigos
from model.persona import Persona
from model.estudiante import Estudiante
from schemas.usuario_schema import usuarios_schema, usuario_schema
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

usuario_routes = Blueprint('usuario_routes', __name__)

@usuario_routes.route('/usuario/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password').encode('utf-')
    
    usuario = Usuario.query.filter_by(email=email).first()
    person = Persona.query.filter_by(user_id=usuario.id).first()
    student = Estudiante.query.filter_by(person_id=person.id).first()
    codigo = Codigos.query.filter_by(code=student.codigo_estudiante).first()
    
    if not usuario:
        data={
            'message': 'Usuario no encontrado',
            'status': 404
        }
        return make_response(jsonify(data),404)
    
    if not usuario and bcrypt.checkpw(password, usuario.password.encode('utf-8')):
        data={
            'message': 'Contraseña incorrecta',
            'status': 400
        }
        return make_response(jsonify(data), 400)
    
    data={
        'message': 'Inició de sesión exitoso',
        'access_token': create_access_token(identity=codigo.code, additional_claims={"id_usuario":usuario.id}),
        'refresh_token': create_refresh_token(identity=codigo.code),
    }
    return make_response(jsonify(data), 200)

@usuario_routes.route('/usuario/listar', methods={'GET'})
def get_usuario():
    all_usuarios = Usuario.query.all()
    result = usuarios_schema.dump(all_usuarios)
    data = {
        'message': 'Todas las filas de la tabla usuario recuperadas',
        'status': 200,
        'data': result
    }
    
    return make_response(jsonify(data), 200)

@usuario_routes.route('/usuario', methods=['POST'])
def create_Usuario():
    
    email = request.json.get('email')
    password = request.json.get('password')
    
    if not email or not password:
        return make_response(jsonify({'message': 'Email y contraseña son requeridos', 'status': 400}), 400)
    
    new_usuario = Usuario(email, password)
    
    db.session.add(new_usuario)
    db.session.commit()
    
    result = usuario_schema.dump(new_usuario)
    
    data={
        'message': 'Nuevo usuario ingresado correctamente',
        'status': 201,
        'data': result
    }
    
    return make_response(jsonify(data),201)

@usuario_routes.route('/usuario/delete', methods=['DELETE'])
def delete():
    
    result = {}
    body = request.get_json()
    id = body.get('id')
    
    if id is None:
        return jsonify({"error": "Falta el id en el body"}), 400
    
    usuario = Usuario.query.get(id)
    if usuario is None:
        return jsonify({"error": f"Usuario con id {id} no fue hallado"}), 404
    
    db.session.delete(usuario)
    db.session.commit()
    
    result["data"]=usuario
    result["status_code"]=200
    result["msg"]="Se eliminó el usuario"
    
    return jsonify(result), 200

@usuario_routes.route('/usuario/update', methods=['POST'])
def update():
    
    result = {}
    body = request.get_json()
    id = body.get('id')
    email = body.get('email')
    password = body.get('password')
    
    if not email or not password:
        return jsonify({'error': 'email y password se requieren'}), 400
    
    usuario = Usuario.query.get(id)
    
    if usuario is None:
        return jsonify({"error": f"Usuario con id {id} no fue encontrado"}),404
    
    usuario.id = id
    usuario.email = email
    
    passworda = usuario.hash_password(password)
    
    usuario.password = passworda
    
    db.session.commit()
    
    result["data"] = usuario
    result["status_code"] = 202
    result["msg"] = "Se modificó el usuario sin convenientes"
    
    return jsonify(result), 202