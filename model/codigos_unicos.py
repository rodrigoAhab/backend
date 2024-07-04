from utils.db import db
from dataclasses import dataclass

@dataclass
class Codigos(db.Model):
    __tablename__= 'unique_codes'
    
    id: int
    code: str
    
    id=db.Column(db.Integer, primary_key=True)
    code=db.Column(db.String(8))
    
    def __init__(self, code):
        self.code = code