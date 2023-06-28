from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from .cadastro.login import auth
from .carrinho_compra.carrinho import carrinho
from .database import db
from .model import Pessoa
from .produtos.produto import produt


def create_app():
    app = Flask(__name__)
    login_manager = LoginManager()
    login_manager.init_app(app)
    app.config["SECRET_KEY"] = "tudo posso naquele que me fortalece"
    csrf = CSRFProtect()
    csrf.init_app(app)
    app.register_blueprint(auth)
    app.register_blueprint(produt)
    app.register_blueprint(carrinho)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    Migrate(app, db)

    @login_manager.user_loader
    def load_user(user_id):
        return Pessoa.query.get(int(user_id))

    @app.cli.command("create_tables")
    def create_tables_command():
        db.create_all()
        print("Tabelas criadas com sucesso!")

    return app


if __name__ == "__main__":
    create_app()
