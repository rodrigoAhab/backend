from utils.db import db
from dataclasses import dataclass
from model.test import Test

@dataclass
class Diagnostico(db.Model):
    __tablename__='diagnosis'
    
    id: int
    test_id: int
    min_score: int
    max_score: int
    diagnosis_text: str
    
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'))
    min_score = db.Column(db.Integer)
    max_score = db.Column(db.Integer)
    diagnosis_text = db.Column(db.Text)
    
    test = db.relationship('Test', backref='diagnosis')
    
    def __init__(self, test_id, min_score, max_score, diagnosis_text):
        self.test_id = test_id
        self.min_score = min_score
        self.max_score = max_score
        self.diagnosis_text = diagnosis_text