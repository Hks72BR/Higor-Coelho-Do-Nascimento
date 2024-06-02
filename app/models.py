from datetime import datetime
from app import db

class Portador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)

    def __repr__(self):
        return f'<Portador {self.nome_completo} - {self.cpf}>'

class Conta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10), unique=True, nullable=False)
    agencia = db.Column(db.String(6), nullable=False)
    saldo = db.Column(db.Float, default=0.0)
    ativa = db.Column(db.Boolean, default=True)
    bloqueada = db.Column(db.Boolean, default=False)
    portador_id = db.Column(db.Integer, db.ForeignKey('portador.id'), nullable=False)
    portador = db.relationship('Portador', backref=db.backref('contas', lazy=True))

    def __repr__(self):
        return f'<Conta {self.numero} - Agencia {self.agencia}>'
