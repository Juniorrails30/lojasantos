from flask import Blueprint, redirect, render_template, request, url_for
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
from flask_login import current_user, login_user, logout_user
from flask_wtf.csrf import validate_csrf

from ..database import db
from ..model import Pessoa

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for("auth.perfil"))
    if request.method == "POST":
        validate_csrf(request.form.get("csrf_token"))

        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        senha_hash = generate_password_hash(senha)
        print(senha_hash)
        nova_pessoa = Pessoa(
            nome,
            email,
            senha_hash,
        )
        db.session.add(nova_pessoa)
        db.session.commit()

        return redirect(url_for("auth.login"))
    return render_template("auth/register.html")


@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        validate_csrf(request.form.get("csrf_token"))

        email = request.form.get("email")
        senha = request.form.get("senha")
        pessoa = Pessoa.query.filter_by(email=email).first()
        if pessoa and check_password_hash(pessoa.senha, senha):
            login_user(pessoa)
            return redirect(url_for("produtos.home"))
    return render_template("auth/login.html")


@auth.route("/perfil")
def perfil():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))
    else:
        return render_template("auth/perfil.html", nome=current_user.nome)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("produtos.home"))


@auth.route("/recuperar", methods=["POST", "GET"])
def recuperar():
    return render_template("auth/recuperar_senha.html")
