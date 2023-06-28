import re

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import current_user, login_user, logout_user
from flask_wtf.csrf import validate_csrf
from password_strength import PasswordPolicy

from ..database import db
from ..model import Pessoa

password_policy = PasswordPolicy()


def check_password_strength(password):
    errors = password_policy.test(password)
    strength = "Senha forte" if not errors else "Senha fraca"
    return strength, errors


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

        # Verifica se o e-mail já existe na base de dados
        pessoa_existente = Pessoa.query.filter_by(email=email).first()
        if pessoa_existente:
            flash("E-mail já cadastrado. Por favor, utilize outro e-mail.")

        password_strength, password_suggestions = check_password_strength(senha)
        if not re.search(r"\W", senha) or not any(c.isupper() for c in senha):
            return render_template(
                "auth/register.html",
                password_strength=password_strength,
                password_suggestions=password_suggestions,
            )

        senha_hash = generate_password_hash(senha)
        nova_pessoa = Pessoa(nome, email, senha_hash)
        db.session.add(nova_pessoa)
        db.session.commit()

    return render_template("auth/register.html")


@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        validate_csrf(request.form.get("csrf_token"))
        email = request.form.get("email")
        senha = request.form.get("senha")
        pessoa = Pessoa.query.filter_by(email=email).first()
        if not pessoa:
            flash("E-mail não cadastrado!")

        elif pessoa and not check_password_hash(pessoa.senha, senha):
            flash("Senha inválida!")

        else:
            login_user(pessoa)
            return redirect(url_for("produtos.home"))
    return render_template("auth/register.html")


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
