from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = ('mysql+pymysql://flask:flask123@localhost/aluguel_veiculos')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'uma-chave-secreta-bem-segura'

    # Inicializa extensões
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Importa e registra blueprints
    from app.auth.routes import auth_bp
    from app.usuarios.routes import usuarios_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(usuarios_bp)

    # Importa models (IMPORTANTE)
    from .models import Usuario, Veiculo, Cliente, Aluguel

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    return app
