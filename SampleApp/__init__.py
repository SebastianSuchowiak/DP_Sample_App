import logging
import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from acl_orm.SQLinterceptor import SQLinterceptor
import os

db = SQLAlchemy()
login_manager = LoginManager()
sqlinterceptor = SQLinterceptor()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if not os.path.exists(os.getcwd()+"/logs"):
        os.mkdir(os.getcwd()+"/logs")
    #logging.basicConfig(filename='SampleApp/logs/app.log', filemode='w', level=logging.DEBUG, format='[%(asctime)s] - [%(levelname)s] - %(message)s')
    #logging.debug("Application started")

    DB_USER = 'postgres'
    DB_PASSWORD = '123'
    DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@localhost/projekt_test3'

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

    from SampleApp.API import employee, salary, address
    app.register_blueprint(employee.bp)
    app.register_blueprint(salary.bp)
    app.register_blueprint(address.bp)

    from SampleApp.API import login
    app.register_blueprint(login.bp)

    login_manager_init(app)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app


def db_init(app):
    print('db_init')
    db.app = app
    db.init_app(app)

    import SampleApp.DataManagement.db


    db.create_all()
    clear_data()
    from SampleApp.populate.populate import populate_employees
    populate_employees(db, 100)

    db.session.commit()
    sqlinterceptor.start(db,tree_file="/home/sebastian/PycharmProjects/backend/SampleApp/sampleroles.txt",acl_file="/home/sebastian/PycharmProjects/backend/SampleApp/sampleacl.txt")
    ## run once
    #sqlinterceptor.assign_role("u1","Role1")
    sqlinterceptor.select_user("u1")


def login_manager_init(app):
    print('login_manager_init')
    login_manager.init_app(app)


def clear_data():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table %s' % table)
        db.session.execute(table.delete())
    db.session.execute('ALTER SEQUENCE employee_id_seq RESTART WITH 1')
    db.session.commit()