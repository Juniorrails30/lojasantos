from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from .cadastro.login import auth
from .database import db
from .model import Pessoa
from .produtos.home import produto


def create_app():
    app = Flask(__name__)
    login_manager = LoginManager()
    login_manager.init_app(app)
    app.config["SECRET_KEY"] = "tudo posso naquele que me fortalece"
    app.register_blueprint(auth)
    app.register_blueprint(produto)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    bcrypt = Bcrypt(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Pessoa.query.get(int(user_id))

    @app.cli.command("create_tables")
    def create_tables_command():
        db.create_all()
        print("Tabelas criadas com sucesso!")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
