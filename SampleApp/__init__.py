from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from acl_orm.SQLinterceptor import SQLinterceptor

db = SQLAlchemy()
login_manager = LoginManager()
sqlinterceptor = SQLinterceptor()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)


    DB_USER = 'postgres'
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
    sqlinterceptor.start(db,tree_file="sampleroles.txt")

def login_manager_init(app):
    print('login_manager_init')
    login_manager.init_app(app)