from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/aluguel_veiculos'    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'uma-chave-secreta-bem-segura'

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' 

    from app.auth.routes import auth_bp
    from app.usuarios.routes import usuarios_bp
    from app.veiculos.routes import veiculos_bp
    from app.alugueis.routes import alugueis_bp
    from app.clientes.routes import clientes_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(veiculos_bp)
    app.register_blueprint(alugueis_bp)
    app.register_blueprint(clientes_bp)

    @app.errorhandler(403)
    def acesso_proibido(e):
        return render_template('403.html'), 403

    from .models import Usuario, Veiculo, Cliente, Aluguel, Manutencao, Pagamento
    with app.app_context():
        db.create_all() 

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    return app