from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from model.persona import Persona
from schemas.persona_schema import persona_schema, personas_schema

persona_routes = Blueprint('persona_routes', __name__)

@persona_routes.route('/persona/lista', methods=['GET'])
def get_Personas():
    personas = Persona.query.all()
    result = personas_schema.dump(personas)
    data = {
        'message': 'Todos las personas de la tabla recuperadas exitosamente',
        'status': 200,
        'data': result
    }
    
    return make_response(jsonify(data), 200)

@persona_routes.route('/persona/add', methods=['POST'])
def create_persona():
    user_id = request.json.get('user_id')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    role = request.json.get('role')
    
    new_persona = Persona(first_name, last_name, role, user_id)
    
    db.session.add(new_persona)
    db.session.commit()
    
    result = persona_schema.dump(new_persona)
    
    data = {
        'message': 'Nueva persona creada!',
        'status': 201,
        'data': result
    }
    
    return make_response(jsonify(data), 201)

@persona_routes.route('/persona/update', methods=['POST'])
def update_persona():
    result = {}
    body = request.get_json()
    
    id = body.get('id')
    first_name = body.get('first_name')
    last_name = body.get('last_name')
    role = body.get('role')
    
    if not first_name or not last_name or not role: 
        return jsonify({'error': 'Nombres, apellidos y rol se requieren'}), 400
    
    persona = Persona.query.get(id)
    
    if Persona is None:
        return jsonify({'error': f"Persona con id {id} no fue encontrado"}), 404
    
    persona.id = id
    persona.first_name = first_name
    persona.last_name = last_name
    persona.role = role
    persona.user_id = persona.user_id
    
    db.session.commit()
    
    result["data"] = persona
    result["status_code"] = 202
    result["msg"] = "Se modificó la persona sin convenientes"
    
    return jsonify(result), 202

@persona_routes.route('/persona/delete', methods=['DELETE'])
def delete_persona():
    result = {}
    body = request.get_json()
    id = body.get('id')
    
    if id is None:
        return jsonify({"error": "Falta el id en el body"}), 400
    
    persona = Persona.query.get(id)
    if persona is None:
        return jsonify({"error": f"Persona con id {id} no fue hallado"}), 404
    
    db.session.delete(persona)
    db.session.commit()
    
    result["data"]=persona
    result["status_code"]=200
    result["msg"]="Se eliminó la persona"
    
    return jsonify(result), 200