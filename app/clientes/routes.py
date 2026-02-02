from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Cliente
from app import db

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes')
def listar():
    clientes = Cliente.query.all()
    return render_template('clientes/listar_cliente.html', clientes=clientes)

@clientes_bp.route('/clientes/novo', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        novo_cliente = Cliente(
            nome=request.form.get('nome'),
            cpf=request.form.get('cpf'),
            cnh=request.form.get('cnh'),
            email=request.form.get('email'),
            telefone=request.form.get('telefone'),
            endereco=request.form.get('endereco')
        )
        db.session.add(novo_cliente)
        db.session.commit()
        flash('Cliente cadastrado com sucesso!')
        return redirect(url_for('clientes.listar'))
    
    return render_template('clientes/cadastrar_cliente.html')

@clientes_bp.route('/clientes/excluir/<int:id>')
def excluir(id):
    cliente = Cliente.query.get_or_404(id)
    try:
        db.session.delete(cliente)
        db.session.commit()
        flash(f'Cliente {cliente.nome} removido com sucesso!')
    except Exception:
        db.session.rollback()
        flash('Erro ao excluir: verifique se o cliente possui aluguéis ativos.')
    return redirect(url_for('clientes.listar'))