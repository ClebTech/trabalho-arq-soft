from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Veiculo
from app import db

veiculos_bp = Blueprint('veiculos', __name__)

@veiculos_bp.route('/')
def index():
    """Resolve o erro 404 da página raiz e renderiza o painel inicial."""
    return render_template('index.html')

@veiculos_bp.route('/veiculos')
def listar():
    veiculos = Veiculo.query.all()
    return render_template('veiculos/listar_veiculo.html', veiculos=veiculos)

@veiculos_bp.route('/veiculos/novo', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        flash('Funcionalidade de cadastro em desenvolvimento!')
        return redirect(url_for('veiculos.listar')) # Redirecionamento via Blueprint
    
    return render_template('veiculos/cadastrar_veiculo.html')