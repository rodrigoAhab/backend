from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from model.diagnostico import Diagnostico

diagnostico_routes = Blueprint('diagnostico_routes', __name__)

@diagnostico_routes.route('/diagnostico/add', methods=['POST'])
def add_diagnoses():
    data = request.get_json()
    diagnoses = []
    for diagnosis_data in data:
        new_diagnosis = Diagnostico(
            test_id=diagnosis_data['test_id'],
            min_score=diagnosis_data['min_score'],
            max_score=diagnosis_data['max_score'],
            diagnosis_text=diagnosis_data['diagnosis_text']
        )
        db.session.add(new_diagnosis)
        diagnoses.append(new_diagnosis)
    
    db.session.commit()
    
    result = [
        {
            'id': diagnosis.id,
            'test_id': diagnosis.test_id,
            'min_score': diagnosis.min_score,
            'max_score': diagnosis.max_score,
            'diagnosis_text': diagnosis.diagnosis_text
        }
        for diagnosis in diagnoses
    ]
    
    return make_response(jsonify(result), 201)
