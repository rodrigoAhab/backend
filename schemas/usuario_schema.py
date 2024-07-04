from utils.ma import ma
from marshmallow import fields

class UsuarioSchema(ma.Schema):
    id = fields.Integer()
    email = fields.String()
    password = fields.String()
    
usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many = True)