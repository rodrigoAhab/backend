from utils.db import db
from dataclasses import dataclass

@dataclass
class Test(db.Model):
    __tablename__ = 'test'
    
    id: int 
    test_name: str
    
    id = db.Column(db.Integer, primary_key = True)
    test_name = db.Column(db.String(255))
    
    def __init__(self, test_name):
        self.test_name = test_name
        
