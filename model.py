from flask_login import UserMixin

from .database import db


class Pessoa(UserMixin, db.Model):
    __tablename__ = "pessoa"
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
    produtos = db.relationship("Produtos", backref="pessoa", lazy=True)

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


class Produtos(db.Model):
    __tablename__ = "produtos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    preco = db.Column(db.Integer)
    quantidade = db.Column(db.Integer)
    pessoa_id = db.Column(db.Integer, db.ForeignKey("pessoa.id"), nullable=False)

    def __init__(self, nome, preco, quantidade, pessoa_id):
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.pessoa_id = pessoa_id


class Carrinho(db.Model):
    __tablename__ = "carrinho"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("pessoa.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)
    quantidade = db.Column(db.Integer, default=1)
    produto = db.relationship("Produtos", backref="carrinho")

    def get_total(self):
        total = 0.0
        total += self.produto.preco * self.quantidade
        return total
