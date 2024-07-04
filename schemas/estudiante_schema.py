from utils.ma import ma
from model.estudiante import Estudiante
from schemas.persona_schema import PersonaSchema
from schemas.codigos_schema import CodigoSchema

class EstudianteSchema(ma.Schema):
    class Meta:
        model = Estudiante
        fields = ('id','person_id','codigo_estudiante','facultad','persona','codigo')
        
    persona = ma.Nested(PersonaSchema) 
    codigo = ma.Nested(CodigoSchema)
    
estudiante_schema = EstudianteSchema()
estudiantes_schema = EstudianteSchema(many = True)