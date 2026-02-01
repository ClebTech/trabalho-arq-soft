from flask import render_template, request, redirect, url_for
from flask_login import login_required
from app.models import Usuario
from app import db
from . import usuarios_bp

@usuarios_bp.route('/')
@login_required
def listar():
    usuarios = Usuario.query.all()
    return render_template('usuarios/listar.html', usuarios=usuarios)

@usuarios_bp.route('/criar', methods=['GET', 'POST'])
@login_required
def criar():
    if request.method == 'POST':
        usuario = Usuario(
            nome=request.form['nome'],
            cpf=request.form['cpf'],
            email=request.form['email'],
            login=request.form['login'],
            senha=request.form['senha'],
            nivel=request.form['nivel']
        )
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('usuarios.listar'))

    return render_template('criar.html')

