from flask import Flask
from utils.db import db
from services.usuario_routes import usuario_routes
from services.persona_routes import persona_routes
from services.estudiante_routes import estudiante_routes
from services.testCompleto_routes import test_routes
from services.diagnostico_routes import diagnostico_routes
from services.resultado_routes import resultados_routes
from config import DATABASE_CONNECTION
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta



app = Flask(__name__)

app.config['SECRET_KEY']='97017582b69247b8a8a88491e108c1ca'
app.config['JWT_SECRET_KEY']='9aa6fe2ac33742958ef600ffea2230fc'
app.config['JWT_ACCESS_TOKEN_EXPIRES']=timedelta(hours=2)
app.config['JWT_REFRESH_TOKEN_EXPIRES']=timedelta(days=1)

jwt=JWTManager(app)

cors = CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION

db.init_app(app)
app.register_blueprint(usuario_routes)
app.register_blueprint(persona_routes)
app.register_blueprint(estudiante_routes)
app.register_blueprint(test_routes)
app.register_blueprint(diagnostico_routes)
app.register_blueprint(resultados_routes)

with app.app_context():
    db.create_all()
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)