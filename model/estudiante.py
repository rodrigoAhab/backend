from utils.db import db
from dataclasses import dataclass
from model.usuario import Usuario
from model.codigos_unicos import Codigos

@dataclass
class Estudiante(db.Model):
    __tablename__ = 'student'
    
    id: int 
    person_id: int 
    codigo_estudiante: str
    facultad: str 
    
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    codigo_estudiante = db.Column(db.String(8), db.ForeignKey('unique_codes.code'))
    facultad = db.Column(db.String(50))
    
    person = db.relationship('Persona', backref = 'student')
    unique_codes = db.relationship('Codigos', backref = 'student')
    
    def __init__(self, person_id, codigo_estudiante, facultad):
        self.person_id = person_id
        self.codigo_estudiante = codigo_estudiante
        self.facultad = facultad