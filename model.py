from flask_login import UserMixin

from .database import db


class Pessoa(UserMixin, db.Model):
    __tablename__ = "pessoa"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    senha = db.Column(db.String)
    cart_quantity = db.Column(db.Integer, default=0)
    produtos = db.relationship("Produtos", backref="pessoa", lazy=True)

    def __init__(
        self,
        nome,
        email,
        senha,
    ):
        self.nome = nome
        self.email = email
        self.senha = senha


class Produtos(db.Model):
    __tablename__ = "produtos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    preco = db.Column(db.Integer)
    categoria = db.Column(db.String)
    quantidade = db.Column(db.Integer)
    pessoa_id = db.Column(db.Integer, db.ForeignKey("pessoa.id"), nullable=False)

    def __init__(self, nome, preco, categoria, quantidade, pessoa_id):
        self.nome = nome
        self.preco = preco
        self.categoria = categoria
        self.quantidade = quantidade
        self.pessoa_id = pessoa_id


class Carrinho(db.Model):
    __tablename__ = "carrinho"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("pessoa.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)
    quantidade = db.Column(db.Integer, default=1)

    # Adicione a relação com o modelo Produtos
    produto = db.relationship("Produtos", backref="carrinho")

    def get_total(self):
        total = 0.0
        total += self.produto.preco * self.quantidade
        return total
