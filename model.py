from flask_login import UserMixin

from .database import db


class Pessoa(UserMixin, db.Model):
    __tablename__ = "Pessoa"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    sobrenome = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    senha = db.Column(db.String)
    telefone = db.Column(db.Integer)
    rua = db.Column(db.String)
    bairro = db.Column(db.String)
    complemento = db.Column(db.String)
    cep = db.Column(db.Integer)
    produtos = db.relationship("produtos", backref="dono", lazy=True)

    def __init__(
        self,
        nome,
        sobrenome,
        email,
        senha,
        telefone,
        rua,
        bairro,
        complemento,
        cep,
    ):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.rua = rua
        self.bairro = bairro
        self.complemento = complemento
        self.cep = cep


class produtos(db.Model):
    __tablename__ = "produtos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    preco = db.Column(db.String)
    quantidade = db.Column(db.String, unique=True)
    dono_id = db.Column(db.Integer, db.ForeignKey("Pessoa.id"), nullable=False)

    def __init__(self, nome, preco, quantidade, dono_id):
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.dono_id = dono_id
