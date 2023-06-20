from flask import Blueprint, redirect, render_template, request, url_for
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
from flask_login import current_user, login_required, login_user, logout_user

from ..database import db
from ..model import Pessoa

auth = Blueprint("auth", __name__)


@auth.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if current_user.is_authenticated:
        # O usuário já está logado, redirecione para a página de perfil
        return redirect(url_for("auth.perfil"))
    if request.method == "POST":
        nome = request.form.get("nome")
        sobrenome = request.form.get("sobrenome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        telefone = request.form.get("telefone")
        rua = request.form.get("rua")
        bairro = request.form.get("bairro")
        complemento = request.form.get("comple")
        cep = request.form.get("cep")
        print(senha)
        senha_hash = generate_password_hash(senha)
        print(senha_hash)
        nova_pessoa = Pessoa(
            nome,
            sobrenome,
            email,
            senha_hash,
            telefone,
            rua,
            bairro,
            complemento,
            cep,
        )
        db.session.add(nova_pessoa)
        db.session.commit()

        return redirect(url_for("auth.login"))
    return render_template("auth/register.html")


@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        pessoa = Pessoa.query.filter_by(email=email).first()
        if pessoa and check_password_hash(pessoa.senha, senha):
            remember = bool(request.form.get("remember"))

            login_user(pessoa, remember=remember)
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
