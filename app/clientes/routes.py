from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.models import Cliente
from app import db

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes')
@login_required
def listar():
    if current_user.nivel == 'Mecânico':
        flash('Acesso negado: Seu perfil não tem permissão para gerenciar clientes.')
        return redirect(url_for('auth.index'))
    
    clientes = Cliente.query.all()
    return render_template('clientes/listar_cliente.html', clientes=clientes)

@clientes_bp.route('/clientes/novo', methods=['GET', 'POST'])
@login_required
def cadastrar():
    if current_user.nivel == 'Mecânico':
        abort(403)

    if request.method == 'POST':
        try:
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
        except Exception as e:
            db.session.rollback()
            flash('Erro ao cadastrar: Verifique se o CPF ou CNH já existem.')
    
    return render_template('clientes/cadastrar_cliente.html')

@clientes_bp.route('/clientes/excluir/<int:id>')
@login_required
def excluir(id):
    if current_user.nivel != 'Administrador':
        flash('Acesso negado: Apenas administradores podem excluir clientes.')
        return redirect(url_for('clientes.listar'))

    cliente = Cliente.query.get_or_404(id)
    try:
        db.session.delete(cliente)
        db.session.commit()
        flash(f'Cliente {cliente.nome} removido com sucesso!')
    except Exception:
        db.session.rollback()
        flash('Erro ao excluir: Este cliente possui aluguéis vinculados no sistema.')
    return redirect(url_for('clientes.listar'))