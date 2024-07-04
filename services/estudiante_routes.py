from sqlite3 import IntegrityError
from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from model.estudiante import Estudiante
from model.usuario import Usuario
from model.codigos_unicos import Codigos
from model.persona import Persona
from schemas.estudiante_schema import estudiante_schema, estudiantes_schema
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

estudiante_routes = Blueprint('estudiante_routes', __name__)

@estudiante_routes.route('/estudiante/add', methods=['POST'])
def create_Estudiantes():
    try:
        # Extraer datos del JSON
        email = request.json['email']
        password = request.json['password']
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        facultad = request.json['facultad']
        code = request.json['codigo_estudiante']

        # Verificar si el email ya existe
        if Usuario.query.filter_by(email=email).first():
            return jsonify({'message': 'El email ya está registrado'}), 400

        # Crear un nuevo usuario
        #hashed_password = generate_password_hash(password, method='sha256')
        new_user = Usuario(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        # Crear una nueva persona asociada al usuario
        new_person = Persona(first_name=first_name, last_name=last_name, role='estudiante', user_id=new_user.id)
        db.session.add(new_person)
        db.session.commit()

        # Generar código único de 8 dígitos
        #code = f"{db.session.execute('SELECT nextval(\'code_sequence\')').scalar():08d}"

        # Crear una nueva entrada en unique_codes
        new_code = Codigos(code=code)
        db.session.add(new_code)
        db.session.commit()

        # Crear un nuevo estudiante
        new_student = Estudiante(person_id=new_person.id, codigo_estudiante=code, facultad=facultad)
        db.session.add(new_student)
        db.session.commit()
        
        data={
            'message': 'Estudiante creado con exito',
            'status': 200,
            'estudiante':estudiante_schema.dump(new_student)
        }
        return make_response(jsonify(data),200)

        return jsonify({
            'message': 'Nuevo estudiante creado exitosamente',
            'student': {
                'id': new_student.id,
                'person_id': new_student.person_id,
                'codigo_estudiante': new_student.codigo_estudiante,
                'facultad': new_student.facultad
            }
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Error al crear el estudiante, posiblemente el código o el email ya existen'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al crear el estudiantee: {str(e)}'}), 500
    
@estudiante_routes.route('/estudiante/listar', methods=['GET'])
def get_Estudiantes():
    students = Estudiante.query.join(Persona, Estudiante.person_id == Persona.id).all()
    
    ##parte para no cagarla
    result={}
    result["data"]=[
        {
            'id': student.id,
            'first_name': student.person.first_name,
            'last_name': student.person.last_name,
            'email': student.person.usuario.email,
            'student_code': student.codigo_estudiante,
            'facultad': student.facultad
        } for student in students
    ]
    return jsonify(result),200
    ##muere nono
    """result = [
        {
            'id': student.id,
            'first_name': student.person.first_name,
            'last_name': student.person.last_name,
            'email': student.person.usuario.email,
            'student_code': student.codigo_estudiante,
            'facultad': student.facultad
        } for student in students
    ]
    return make_response(jsonify({'Estudiantes': result}), 200)"""

@estudiante_routes.route('/estudiante/delete', methods=['DELETE'])
def delete_Estudiante():
    email = request.json.get('email')
    user = Usuario.query.filter_by(email=email).first()
    if user:
        person = Persona.query.filter_by(user_id=user.id).first()
        if person:
            student = Estudiante.query.filter_by(person_id=person.id).first()
            if student:
                codigo = Codigos.query.filter_by(code=student.codigo_estudiante).first()
                if codigo:
                    db.session.delete(student)
                    db.session.delete(person)
                    db.session.delete(codigo)
                    db.session.delete(user)
                    
                    db.session.commit()

                    return make_response(jsonify({'message': 'Estudiante eliminado :D'}), 200)
                return make_response(jsonify({'message': 'Codigo de estudiante no hallado'}), 404)
            return make_response(jsonify({'message': 'Estudiante no encontrado'}), 404)
        return make_response(jsonify({'message': 'Persona no hallada'}), 404)
    return make_response(jsonify({'message': 'Usuario no hallado'}), 404)

@estudiante_routes.route('/estudiante/update', methods=['PUT']) #este metodo no actualiza correo ni contraseña del estudiante
def update_student():
    email = request.json.get('email') #importante colocar el email del estudiante a actualizar
    new_first_name = request.json.get('first_name')
    new_last_name = request.json.get('last_name')
    new_facultad = request.json.get('facultad')
    
    user = Usuario.query.filter_by(email=email).first()
    if user:
        person = Persona.query.filter_by(user_id=user.id).first()
        if person:
            student = Estudiante.query.filter_by(person_id=person.id).first()
            if student:
                if new_first_name:
                    person.first_name = new_first_name
                if new_last_name:
                    person.last_name = new_last_name
                if new_facultad:
                    student.facultad = new_facultad
                
                db.session.commit()
                return make_response(jsonify({'message': 'Datos del estudiante actualizado'}), 200)
            return make_response(jsonify({'message': 'Estudiante no encontrado'}), 404)
        return make_response(jsonify({'message': 'Persona no hallada'}), 404)
    return make_response(jsonify({'message': 'Usuario no hallado'}), 404)

@estudiante_routes.route('/estudiante/search', methods=['GET'])
def get_student_by_code():
    student_code = request.json.get('codigo_estudiante')
    
    if student_code:
        student = Estudiante.query.filter_by(codigo_estudiante=student_code).first()
        
        if student:
            person = Persona.query.filter_by(id=student.person_id).first()
            
            if person:
                student_data = {
                    'id': student.id,
                    'codigo_estudiante': student.codigo_estudiante,
                    'facultad': student.facultad,
                    'person': {
                        'id': person.id,
                        'first_name': person.first_name,
                        'last_name': person.last_name,
                        'role': person.role,
                        'user_id': person.user_id
                    }
                }
                return make_response(jsonify({'message': 'Estudiante encontrado!', 'data': student_data}), 200)
            return make_response(jsonify({'message': 'Persona no hallada'}), 404)
        return make_response(jsonify({'message': 'Estudiante no encontrado'}), 404)
    
    return make_response(jsonify({'message': 'Coloque el código del estudiante'}), 400)

@estudiante_routes.route('/estudiante/buscarPorEmail', methods=['GET'])
def get_student_by_email():
    email = request.args.get('email')
    if not email:
        return jsonify({'message': 'Email is required'}), 400

    user = Usuario.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    person = Persona.query.filter_by(user_id=user.id).first()
    if not person:
        return jsonify({'message': 'Person not found'}), 406

    student = Estudiante.query.filter_by(person_id=person.id).first()
    if not student:
        return jsonify({'message': 'Student not found'}), 407
    

    result = {}
    result["data"]=[
        {
        'id': student.id,
        'first_name': student.person.first_name,
        'last_name': student.person.last_name,
        'email': user.email,
        'student_code': student.codigo_estudiante,
        'facultad': student.facultad,
        'rol': student.person.role,
        }
    ]

    return jsonify(result), 200

