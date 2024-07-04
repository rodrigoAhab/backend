from utils.ma import ma
from marshmallow import fields

class CodigoSchema(ma.Schema):
    id = fields.Integer()
    code = fields.String()
    
codigo_schema = CodigoSchema()
codigos_schema = CodigoSchema(many = True)