from utils.db import db
from dataclasses import dataclass
from model.usuario import Usuario

@dataclass
class Persona(db.Model):
    __tablename__ = 'person'
    id: int 
    first_name: str
    last_name: str
    role: str
    user_id: int 
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    role = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    
    usuario = db.relationship('Usuario', backref='person')
    
    def __init__(self, first_name, last_name, role, user_id):
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.user_id = user_id