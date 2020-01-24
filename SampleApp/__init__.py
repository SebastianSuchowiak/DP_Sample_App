from flask import Flask

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

    from SampleApp.DataManagement import db
    db.db_init(app)

    from SampleApp.API import employee
    app.register_blueprint(employee.bp)

    from SampleApp.TokenLoginManager import token_login_manager
    token_login_manager.login_manager_init(app)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app


