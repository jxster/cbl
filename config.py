import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'better_not'
    SSL_DISABLE = False

    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev-db.sqlite')

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
