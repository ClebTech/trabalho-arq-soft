from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.models import Veiculo
from app import db

veiculos_bp = Blueprint('veiculos', __name__)

@veiculos_bp.route('/veiculos')
@login_required
def listar():
    veiculos = Veiculo.query.all()
    return render_template('veiculos/listar_veiculo.html', veiculos=veiculos)

@veiculos_bp.route('/veiculos/novo', methods=['GET', 'POST'])
@login_required
def novo():
    if current_user.nivel not in ['Administrador', 'Mecânico']:
        flash('Acesso negado: Apenas administradores ou mecânicos podem cadastrar veículos.')
        return redirect(url_for('veiculos.listar'))

    if request.method == 'POST':
        novo_veiculo = Veiculo(
            modelo=request.form.get('modelo'),
            fabricante=request.form.get('fabricante'), 
            tipo=request.form.get('tipo'),
            ano=request.form.get('ano'),
            placa=request.form.get('placa'),
            cor=request.form.get('cor'),
            estado_conservacao=request.form.get('estado_conservacao'),
            status='Disponível'
        )
        try:
            db.session.add(novo_veiculo)
            db.session.commit()
            flash(f'Veículo {novo_veiculo.modelo} cadastrado com sucesso!')
            return redirect(url_for('veiculos.listar'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao cadastrar veículo. Verifique se a placa já existe.')
    
    return render_template('veiculos/cadastrar_veiculo.html')

@veiculos_bp.route('/veiculos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    if current_user.nivel not in ['Administrador', 'Mecânico']:
        abort(403)
        
    veiculo = Veiculo.query.get_or_404(id)
    if request.method == 'POST':
        veiculo.modelo = request.form.get('modelo')
        veiculo.fabricante = request.form.get('fabricante')
        veiculo.tipo = request.form.get('tipo')
        veiculo.ano = request.form.get('ano')
        veiculo.cor = request.form.get('cor')
        veiculo.estado_conservacao = request.form.get('estado_conservacao')
        veiculo.status = request.form.get('status')
        
        try:
            db.session.commit()
            flash('Veículo atualizado com sucesso!')
            return redirect(url_for('veiculos.listar'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao atualizar veículo.')
        
    return render_template('veiculos/editar_veiculo.html', veiculo=veiculo)

@veiculos_bp.route('/veiculos/excluir/<int:id>')
@login_required
def excluir(id):
    if current_user.nivel != 'Administrador':
        flash('Acesso negado: Apenas administradores podem excluir veículos.')
        return redirect(url_for('veiculos.listar'))

    veiculo = Veiculo.query.get_or_404(id)
    try:
        db.session.delete(veiculo)
        db.session.commit()
        flash('Veículo removido da frota.')
    except Exception:
        db.session.rollback()
        flash('Erro ao excluir: O veículo pode estar vinculado a um contrato de aluguel.')
    return redirect(url_for('veiculos.listar'))