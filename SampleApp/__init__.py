from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
login_manager = LoginManager()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)


    DB_USER = 'server'
    DB_PASSWORD = '123'
    DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@localhost/projekt_test'

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        SQLALCHEMY_DATABASE_URI = DATABASE_URL,
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)


    db_init(app)


    from SampleApp.API import employee
    app.register_blueprint(employee.bp)

    login_manager_init(app)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app


def db_init(app):
    print('db_init')
    db.app = app
    db.init_app(app)
    db.create_all()
    db.session.commit()


def login_manager_init(app):
    print('login_manager_init')
    login_manager.init_app(app)