# all the import goodies
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()


# factory method for creating the app
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    #TODO: implemeent config_from_pyfile / instance configs
    #app.config.from_pyfile('config.py')
    bootstrap.init_app(app)
    db.init_app(app)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app