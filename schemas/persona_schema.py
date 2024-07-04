from utils.ma import ma
from model.persona import Persona
from schemas.usuario_schema import UsuarioSchema

class PersonaSchema(ma.Schema):
    class Meta:
        model = Persona
        fields = ('id','first_name','last_name','role','user_id','usuario')
        
    usuario = ma.Nested(UsuarioSchema)

persona_schema = PersonaSchema()
personas_schema = PersonaSchema(many=True)