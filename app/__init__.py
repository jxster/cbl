# all the import goodies
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.assets import Environment, Bundle
from config import config
import os

bootstrap = Bootstrap()
db = SQLAlchemy()


# factory method for creating the app
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    env = Environment(app)

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask.ext.sslify import SSLify
        sslify = SSLify(app)

    #TODO: implement config_from_pyfile / instance configs
    #app.config.from_pyfile('config.py')
    env.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)

    # tell flask-assets where to look
    env.load_path = [
        os.path.join(os.path.dirname(__file__), 'bower_components'),
        os.path.join(os.path.dirname(__file__), 'styles'),
        os.path.join(os.path.dirname(__file__), 'js')
    ]

    env.register(
        'style',
        Bundle(
            'style.scss',
            'player.scss',
            'team.scss',
            filters='scss',
            output='style.css'
        )
    )

    env.register(
        'app',
        Bundle(
            'home.js',
            output='app.js'
        )
    )

    @app.template_filter('datetime')
    def format_gametime(value):
        return value.strftime('%m.%d.%Y %H:%M%p')

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
