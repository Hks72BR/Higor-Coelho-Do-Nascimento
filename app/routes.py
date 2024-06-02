from flask import Blueprint, jsonify, request, abort, current_app as app
from app import db
from app.models import Portador, Conta
from app.validations import validar_cpf
from datetime import datetime

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return jsonify({"message": "Bem-vindo à API Digital Dock!"})

@bp.route('/portadores', methods=['POST'])
def criar_portador():
    data = request.get_json()
    nome_completo = data.get('nome_completo')
    cpf = data.get('cpf')

    if not nome_completo or not cpf:
        abort(400, 'Nome completo e CPF são obrigatórios')

    if not validar_cpf(cpf):
        abort(400, 'CPF inválido')

    if Portador.query.filter_by(cpf=cpf).first():
        abort(400, 'CPF já cadastrado')

    portador = Portador(nome_completo=nome_completo, cpf=cpf)
    db.session.add(portador)
    db.session.commit()
    return jsonify({'id': portador.id, 'nome_completo': portador.nome_completo, 'cpf': portador.cpf}), 201

@bp.route('/portadores/<int:id>', methods=['DELETE'])
def remover_portador(id):
    portador = Portador.query.get_or_404(id)
    # Excluir manualmente todas as contas relacionadas ao portador
    Conta.query.filter_by(portador_id=id).delete()
    db.session.delete(portador)
    db.session.commit()
    return jsonify({'message': 'Portador removido', 'id': id})

import random

def gerar_numero_conta():
    return ''.join([str(random.randint(0, 9)) for _ in range(10)])

def gerar_agencia():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

@bp.route('/contas', methods=['POST'])
def criar_conta():
    data = request.get_json()
    cpf = data.get('cpf')

    portador = Portador.query.filter_by(cpf=cpf).first()
    if not portador:
        abort(404, 'Portador não encontrado')

    conta = Conta(numero=gerar_numero_conta(), agencia=gerar_agencia(), portador=portador)
    db.session.add(conta)
    db.session.commit()
    return jsonify({'id': conta.id, 'numero': conta.numero, 'agencia': conta.agencia, 'saldo': conta.saldo}), 201

@bp.route('/contas/<int:id>', methods=['GET'])
def consultar_conta(id):
    conta = Conta.query.get_or_404(id)
    return jsonify({'numero': conta.numero, 'agencia': conta.agencia, 'saldo': conta.saldo})

@bp.route('/contas/<int:id>/extrato', methods=['GET'])
def consultar_extrato(id):
    conta = Conta.query.get_or_404(id)
    inicio = request.args.get('inicio')
    fim = request.args.get('fim')

    if not inicio or not fim:
        app.logger.error('Parâmetros de data de início e fim não fornecidos')
        abort(400, 'Os parâmetros de data de início e fim são obrigatórios')

    try:
        inicio = datetime.strptime(inicio, '%Y-%m-%d')
        fim = datetime.strptime(fim, '%Y-%m-%d')
    except ValueError:
        app.logger.error('Formato de data inválido')
        abort(400, 'Formato de data inválido. Use AAAA-MM-DD')

    app.logger.info(f'Consultando extrato de {inicio} até {fim}')
    
    # Exemplo de extrato fictício
    extrato = [
        {"data": "2023-01-01", "tipo": "deposito", "valor": 1000},
        {"data": "2023-01-05", "tipo": "saque", "valor": 200},
        {"data": "2023-02-10", "tipo": "deposito", "valor": 500},
    ]

    extrato_filtrado = [transacao for transacao in extrato if inicio <= datetime.strptime(transacao['data'], '%Y-%m-%d') <= fim]

    return jsonify({'extrato': extrato_filtrado})

@bp.route('/contas/<int:id>/fechar', methods=['POST'])
def fechar_conta(id):
    conta = Conta.query.get_or_404(id)
    conta.ativa = False
    db.session.commit()
    return '', 204

@bp.route('/contas/<int:id>/saque', methods=['POST'])
def saque(id):
    conta = Conta.query.get_or_404(id)
    if conta.bloqueada or not conta.ativa:
        abort(403, 'Conta bloqueada ou inativa')

    data = request.get_json()
    valor = data.get('valor')

    if valor is None or valor <= 0:
        abort(400, 'Valor de saque inválido')

    if conta.saldo < valor:
        abort(400, 'Saldo insuficiente')

    conta.saldo -= valor
    db.session.commit()
    return jsonify({'saldo': conta.saldo}), 200

@bp.route('/contas/<int:id>/deposito', methods=['POST'])
def deposito(id):
    conta = Conta.query.get_or_404(id)
    if conta.bloqueada or not conta.ativa:
        abort(403, 'Conta bloqueada ou inativa')

    data = request.get_json()
    valor = data.get('valor')

    if valor is None or valor <= 0:
        abort(400, 'Valor de depósito inválido')

    conta.saldo += valor
    db.session.commit()
    return jsonify({'saldo': conta.saldo}), 200

@bp.route('/contas/<int:id>/bloquear', methods=['POST'])
def bloquear_conta(id):
    conta = Conta.query.get_or_404(id)
    conta.bloqueada = True
    db.session.commit()
    return jsonify({'message': 'Conta bloqueada', 'status': 'bloqueada'})

@bp.route('/contas/<int:id>/desbloquear', methods=['POST'])
def desbloquear_conta(id):
    conta = Conta.query.get_or_404(id)
    conta.bloqueada = False
    db.session.commit()
    return jsonify({'message': 'Conta desbloqueada', 'status': 'desbloqueada'})
