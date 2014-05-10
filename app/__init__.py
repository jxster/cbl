# all the import goodies
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# our app object
app = Flask(__name__)
# loading configs
app.config.from_object('config')

# defining db object
db = SQLAlchemy(app)


from app import views