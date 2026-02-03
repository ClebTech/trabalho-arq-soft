from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.models import Usuario
from app import db
from . import usuarios_bp
from datetime import datetime

@usuarios_bp.route('/')
@login_required
def listar():
    if current_user.nivel != 'Administrador':
        flash('Acesso negado: Você não tem permissão para ver esta página.')
        return redirect(url_for('auth.index'))
        
    usuarios = Usuario.query.all()
    return render_template('usuarios/listar.html', usuarios=usuarios)

@usuarios_bp.route('/criar', methods=['GET', 'POST'])
@login_required
def criar():
    if current_user.nivel != 'Administrador':
        abort(403)

    if request.method == 'POST':
        try:
            usuario = Usuario(
                nome=request.form['nome'],
                cpf=request.form['cpf'],
                email=request.form['email'],
                telefone=request.form.get('telefone'),
                login=request.form['login'],
                senha=request.form['senha'],
                nivel=request.form['nivel'], 
                salario=request.form.get('salario', 0.00)
            )
            db.session.add(usuario)
            db.session.commit()
            flash('Usuário criado com sucesso!')
            return redirect(url_for('usuarios.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao salvar: {e}")
            return redirect(url_for('usuarios.criar'))

    return render_template('usuarios/criar.html')

@usuarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    if current_user.nivel != 'Administrador':
        abort(403)
        
    usuario = Usuario.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            usuario.nome = request.form['nome']
            usuario.email = request.form['email']
            usuario.telefone = request.form.get('telefone')
            usuario.nivel = request.form['nivel']
            usuario.salario = request.form.get('salario')
            
            db.session.commit()
            flash('Dados atualizados com sucesso!')
            return redirect(url_for('usuarios.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao atualizar: {e}")
        
    return render_template('usuarios/editar.html', usuario=usuario)

@usuarios_bp.route('/excluir/<int:id>')
@login_required
def excluir(id):
    if current_user.nivel != 'Administrador':
        flash('Acesso negado.')
        return redirect(url_for('auth.index'))
        
    usuario = Usuario.query.get_or_404(id)
    
    if usuario.id == current_user.id:
        flash('Erro: Você não pode excluir seu próprio usuário enquanto estiver logada.')
        return redirect(url_for('usuarios.listar'))
        
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuário removido do sistema.')
    return redirect(url_for('usuarios.listar'))