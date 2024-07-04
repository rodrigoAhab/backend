from utils.db import db
from dataclasses import dataclass
from model.test import Test

@dataclass
class Pregunta(db.Model):
    __tablename__ = 'question'
    
    id: int
    test_id: str
    question_text: str
    
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'))
    question_text = db.Column(db.Text)
    
    test = db.relationship('Test', backref='question')
    
    def __init__(self, test_id, question_text):
        self.test_id = test_id
        self.question_text = question_text