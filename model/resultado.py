from sqlalchemy import func
from utils.db import db
from dataclasses import dataclass
from model.test import Test
from model.diagnostico import Diagnostico

@dataclass
class Result(db.Model):
    __tablename__ = 'result'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo_entidad = db.Column(db.String(8), db.ForeignKey('unique_codes.code'))
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'))
    total_score = db.Column(db.Integer)
    diagnosis_id = db.Column(db.Integer, db.ForeignKey('diagnosis.id'))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    unique_codes = db.relationship('Codigos', backref='result')
    test = db.relationship('Test', backref='result')
    diagnosis = db.relationship('Diagnostico', backref='result')
    
    def __init__(self, codigo_entidad, test_id, total_score, diagnosis_id, created_at):
        self.codigo_entidad = codigo_entidad
        self.test_id = test_id
        self.total_score = total_score
        self.diagnosis_id = diagnosis_id
        self.created_at = created_at