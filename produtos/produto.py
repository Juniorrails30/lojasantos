from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_wtf.csrf import validate_csrf
from sqlalchemy import exc

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
            "home/index.html",
            produtos=produtos,
            carrinho=carrinho,
            total=total,
            quantidade_produtos=quantidade_produtos,
        )
    else:
        return render_template("home/index.html", produtos=produtos)


@produt.route("/estoque_produtos", methods=["GET"])
@login_required
def listar_produtos():
    produtos = Produtos.query.all()
    return render_template(
        "home/listar_produtos.html",
        produtos=produtos,
    )


@produt.route("/listar_produtos/<string:categoria>", methods=["GET"])
def listar_produtos_categoria(categoria):
    produtos_categoria = Produtos.query.filter_by(categoria=categoria).all()
    return render_template(
        "home/lista_produto_categoria.html",
        produtos_categoria=produtos_categoria,
    )


@produt.route("/add_produtos", methods=["POST", "GET"])
@login_required
def add_post():
    if current_user.email == "admin@santoslojas.com":
        if request.method == "POST":
            validate_csrf(request.form.get("csrf_token"))

            nome = request.form.get("nome")
            preco = request.form.get("preco")
            categoria = request.form.get("categoria")
            quantidade = request.form.get("quantidade")
            novo_produto = Produtos(
                nome,
                preco,
                categoria,
                quantidade,
                current_user.id,
            )
            db.session.add(novo_produto)
            db.session.commit()
        return render_template("home/produtos.html")
    else:
        return redirect(url_for("produtos.home"))


@produt.route("/atualizar_produto/<int:produto_id>", methods=["POST", "GET"])
@login_required
def atualizar_produtos(produto_id):
    produto = Produtos.query.get(produto_id)
    if current_user.email == "admin@santoslojas.com":
        if request.method == "POST":
            nome = request.form.get("nome")
            preco = request.form.get("preco")
            categoria = request.form.get("categoria")
            quantidade = request.form.get("quantidade")

            # Atualize os valores do produto existente
            produto.nome = nome
            produto.preco = preco
            produto.quantidade = quantidade
            produto.categoria = categoria

            db.session.commit()
            flash("Produto atualizado com sucesso")

        return render_template("home/atualizar_produto.html", produto=produto)
    else:
        return redirect(url_for("produtos.home"))


@produt.route("/deleta_produto/<int:produto_id>", methods=["POST", "GET"])
@login_required
def deletar_produto(produto_id):
    produto = Produtos.query.get(produto_id)
    if produto:
        try:
            # Deleta os registros relacionados na tabela carrinho
            Carrinho.query.filter_by(produto_id=produto.id).delete()

            # Deleta o produto do estoque
            db.session.delete(produto)
            db.session.commit()

            flash("Produto deletado com sucesso.", "success")
        except exc.SQLAlchemyError:
            db.session.rollback()
            flash("Erro ao deletar o produto.", "error")
    else:
        flash("Produto não encontrado.", "error")

    return redirect(url_for("produtos.home"))
