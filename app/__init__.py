# all the import goodies
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# our app object
app = Flask(__name__, instance_relative_config=True)
# loading configs
app.config.from_object('config')
app.config.from_pyfile('config.py')

# defining db object
db = SQLAlchemy(app)


from app import views