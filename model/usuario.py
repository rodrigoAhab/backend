from utils.db import db
from dataclasses import dataclass
import bcrypt

@dataclass
class Usuario(db.Model):
    __tablename__= 'usuario'
    id: int
    email: str
    password: str
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    
    def __init__(self, email, password):
        self.email = email
        self.password = self.hash_password(password)
    
    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')