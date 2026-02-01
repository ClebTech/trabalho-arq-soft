from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.models import Usuario
from app import db
from . import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form['login']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(login=login_input).first()

        if usuario and usuario.senha == senha:
            login_user(usuario)
            return redirect(url_for('usuarios.listar'))
        else:
            flash('Login ou senha inválidos')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

