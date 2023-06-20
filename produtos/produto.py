from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..database import db
from ..model import Carrinho, Produtos

produt = Blueprint("produtos", __name__)


@produt.route("/")
def home():
    produtos = Produtos.query.all()
    if current_user.is_authenticated:
        carrinho = Carrinho.query.filter_by(user_id=current_user.id).all()
        quantidade_produtos = {}
        for item in carrinho:
            produto_id = item.produto.id
            if produto_id in quantidade_produtos:
                quantidade_produtos[produto_id] += item.quantidade
            else:
                quantidade_produtos[produto_id] = item.quantidade

        total = 0.0
        for item in carrinho:
            total += item.get_total()

        return render_template(
            "home/home.html",
            produtos=produtos,
            carrinho=carrinho,
            total=total,
            quantidade_produtos=quantidade_produtos,
        )
    else:
        return render_template("home/home.html", produtos=produtos)


@produt.route("/add_produtos", methods=["POST", "GET"])
@login_required
def add_post():
    if current_user.email == "admin@santoslojas.com":
        if request.method == "POST":
            nome = request.form.get("nome")
            preco = request.form.get("preco")
            quantidade = request.form.get("quantidade")
            novo_produto = Produtos(nome, preco, quantidade, current_user.id)
            db.session.add(novo_produto)
            db.session.commit()
        return render_template("home/produtos.html")
    else:
        return redirect(url_for("produtos.home"))


@produt.route("/adicionar_carrinho/<int:produto_id>", methods=["POST"])
@login_required
def add_to_cart(produto_id):
    produto = Produtos.query.get(produto_id)
    if produto:
        carrinho_item = Carrinho.query.filter_by(
            user_id=current_user.id, produto_id=produto.id
        ).first()
        if carrinho_item:
            carrinho_item.quantidade += 1
        else:
            carrinho_item = Carrinho(user_id=current_user.id, produto_id=produto.id)
            db.session.add(carrinho_item)
        db.session.commit()
        flash("Produto adicionado ao carrinho com sucesso.", "success")
    return redirect(url_for("produtos.home"))


@produt.route("/remover_item_carrinho/<int:produto_id>", methods=["POST"])
@login_required
def remove_from_cart(produto_id):
    carrinho_item = Carrinho.query.filter_by(
        user_id=current_user.id, produto_id=produto_id
    ).first()
    if carrinho_item:
        if carrinho_item.quantidade > 1:
            carrinho_item.quantidade -= 1
        else:
            db.session.delete(carrinho_item)
        db.session.commit()
        flash("Item removido do carrinho com sucesso.", "success")
    return redirect(url_for("produtos.home"))
