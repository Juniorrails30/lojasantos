import json

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_wtf.csrf import validate_csrf
from sqlalchemy import func

from ..database import db
from ..model import Carrinho, Produtos

carrinho = Blueprint("carrinho", __name__)


@carrinho.route("/carrinho/contar", methods=["GET"])
def contar_itens_carrinho():
    if current_user.is_authenticated:
        cart_quantity = current_user.cart_quantity
    else:
        cart_quantity = 0

    response = {"cart_count": cart_quantity}
    return json.dumps(response)


@carrinho.route("/cart")
@login_required
def cart():
    carrinho_itens = Carrinho.query.filter_by(user_id=current_user.id).all()
    total = sum(item.produto.preco * item.quantidade for item in carrinho_itens)
    return render_template(
        "home/cart.html",
        carrinho_itens=carrinho_itens,
        total=total,
    )


@carrinho.route("/adicionar_carrinho/<int:produto_id>", methods=["POST"])
def add_to_cart(produto_id):
    if request.method == "POST":
        validate_csrf(request.headers.get("X-CSRFToken"))

    produto = Produtos.query.get(produto_id)
    if produto:
        carrinho_item = Carrinho.query.filter_by(
            user_id=current_user.id, produto_id=produto.id
        ).first()

        if carrinho_item:
            carrinho_item.quantidade += 1
        else:
            carrinho_item = Carrinho(
                user_id=current_user.id,
                produto_id=produto.id,
            )
            db.session.add(carrinho_item)

        db.session.commit()

    # Atualize o campo cart_quantity no modelo Pessoa
    current_user.cart_quantity = (
        db.session.query(func.sum(Carrinho.quantidade))
        .filter_by(user_id=current_user.id)
        .scalar()
    )
    db.session.commit()

    # Retorna a quantidade atualizada de itens no carrinho em formato JSON
    response = {"cart_count": current_user.cart_quantity}
    return json.dumps(response)


@carrinho.route("/remover_item_carrinho/<int:produto_id>", methods=["POST"])
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

    # Atualize o campo cart_quantity no modelo Pessoa
    current_user.cart_quantity = (
        db.session.query(func.sum(Carrinho.quantidade))
        .filter_by(user_id=current_user.id)
        .scalar()
    )
    db.session.commit()

    return redirect(url_for("carrinho.cart"))
