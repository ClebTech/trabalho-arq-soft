from app import create_app, db
from app.models import Usuario, Veiculo, Cliente
from datetime import date

app = create_app()

def seed_database():
    with app.app_context():
        print("Limpando e recriando tabelas...")
        db.drop_all()
        db.create_all()
        
        # 1. Criar Usuário Administrador (Nível deve ser 'Administrador')
        admin = Usuario(
            nome='Administrador Murphy',
            cpf='000.000.000-01',
            email='admin@email.com',
            login='admin',
            senha='123',
            nivel='Administrador', # Deve ser exatamente como no Enum do models.py
            salario=5000.00
        )
        
        # 2. Criar Cliente (Precisa de CPF e CNH obrigatórios)
        cliente = Cliente(
            nome='João da Silva',
            cpf='111.111.111-11',
            cnh='12345678910', # Campo obrigatório no seu models
            email='joao@email.com',
            telefone='(11) 98888-8888'
        )
        
        # 3. Criar Veículo (Campos modelo e placa são obrigatórios)
        veiculo = Veiculo(
            modelo='Corolla',
            fabricante='Toyota',
            ano=2024,
            placa='ABC-1234',
            status='Disponível'
        )

        db.session.add_all([admin, cliente, veiculo])
        
        try:
            db.session.commit()
            print("✅ Sucesso! Tabelas recriadas e dados inseridos.")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro de integridade: {e}")

if __name__ == '__main__':
    seed_database()