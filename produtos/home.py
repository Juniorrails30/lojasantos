from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..database import db
from ..model import produtos

produto = Blueprint("produtos", __name__)


@produto.route("/", methods=["GET"])
def home():
    return render_template("home/home.html", nome=current_user)


@produto.route("/add_produtos", methods=["POST", "GET"])
@login_required
def add_post():
    if current_user.email == "admin@santoslojas.com":
        if request.method == "POST":
            nome = request.form.get("nome")
            preco = request.form.get("preco")
            quantidade = request.form.get("quantidade")
            novo_produto = produtos(nome, preco, quantidade, current_user.id)
            db.session.add(novo_produto)
            db.session.commit()
        return render_template("home/produtos.html", nome=current_user.email)
    else:
        return redirect(url_for("produtos.home"))
