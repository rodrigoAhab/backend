from utils.db import db
from dataclasses import dataclass
from model.pregunta import Pregunta

@dataclass
class Opcion(db.Model):
    __tablename__='option'
    
    id: int
    question_id: int 
    option_text: str
    score: int
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    option_text = db.Column(db.Text)
    score = db.Column(db.Integer)
    
    question = db.relationship('Pregunta', backref='option')
    
    def __init__(self, question_id, option_text, score):
        self.question_id = question_id
        self.option_text = option_text
        self.score = score