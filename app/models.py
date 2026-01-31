from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    data_nascimento = db.Column(db.Date)
    login = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    nivel = db.Column(db.Enum('Administrador', 'Atendente', 'Mecânico'), nullable=False)
    salario = db.Column(db.Numeric(10, 2), default=0.00)

class Cliente(db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    cnh = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20))
    data_nascimento = db.Column(db.Date)
    endereco = db.Column(db.String(200))

class Veiculo(db.Model):
    __tablename__ = 'veiculo'
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(100), nullable=False)
    fabricante = db.Column(db.String(100))
    tipo = db.Column(db.String(50))
    ano = db.Column(db.Integer)
    placa = db.Column(db.String(10), unique=True, nullable=False)
    estado_conservacao = db.Column(db.String(100))
    cor = db.Column(db.String(50))
    caracteristicas = db.Column(db.Text)
    status = db.Column(db.Enum('Disponível', 'Alugado', 'Manutenção'), default='Disponível')

class Aluguel(db.Model):
    __tablename__ = 'aluguel'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id', ondelete='CASCADE'), nullable=False)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculo.id', ondelete='CASCADE'), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date)
    prazo_devolucao = db.Column(db.Date, nullable=False)
    detalhes = db.Column(db.Text)
    valor = db.Column(db.Numeric(10, 2), default=0.00)
    multa = db.Column(db.Numeric(10, 2), default=0.00)
    devolvido = db.Column(db.Boolean, default=False)
    
    # Relacionamentos
    cliente = db.relationship('Cliente', backref=db.backref('alugueis', cascade='all, delete'))
    veiculo = db.relationship('Veiculo', backref=db.backref('alugueis', cascade='all, delete'))

class Manutencao(db.Model):
    __tablename__ = 'manutencoes'
    id = db.Column(db.Integer, primary_key=True)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculo.id', ondelete='CASCADE'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE'), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    data_solicitacao = db.Column(db.Date, nullable=False)
    data_conclusao = db.Column(db.Date)
    status = db.Column(db.Enum('Pendente', 'Em_Andamento', 'Finalizada'), default='Pendente')

class SolicitacaoPeca(db.Model):
    __tablename__ = 'solicitacoes_pecas'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE'), nullable=False)
    nome_peca = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data_solicitacao = db.Column(db.Date, nullable=False)
    justificativa = db.Column(db.Text, nullable=False)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculo.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.Enum('Em_Analise', 'Aprovada', 'Recusada'), default='Em_Analise')

class Relatorio(db.Model):
    __tablename__ = 'relatorios'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE'), nullable=False)
    tipo = db.Column(db.Enum('Financeiro', 'Operacional', 'Salarios'), nullable=False)
    periodoInicio = db.Column(db.Date, nullable=False)
    periodoFim = db.Column(db.Date, nullable=False)
    formato = db.Column(db.Enum('PDF', 'XLSX'), nullable=False)
    data_geracao = db.Column(db.DateTime, default=datetime.utcnow)

class Pagamento(db.Model):
    __tablename__ = 'pagamento'
    id = db.Column(db.Integer, primary_key=True)
    aluguel_id = db.Column(db.Integer, db.ForeignKey('aluguel.id', ondelete='CASCADE'), nullable=False)
    metodo = db.Column(db.Enum('Cartão', 'Pix', 'Dinheiro', 'Boleto'), nullable=False)
    valor_pago = db.Column(db.Numeric(10, 2), nullable=False)
    data_pagamento = db.Column(db.Date, nullable=False)