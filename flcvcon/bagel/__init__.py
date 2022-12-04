from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
# from bagel import storage

app = Flask(__name__)
app.secret_key = 'some secret salt'

SQLALCHEMY_DATABASE_URI = 'database.db'
DEBUG = True
SECRET_KEY = 'some secret salt'
SQLALCHEMY_TRACK_MODIFICATIONS = False

app.config.from_object(__name__)

app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.root_path, 'database.db'),
    DEBUG=True,
    SECRET_KEY='some secret salt',
    SQLALCHEMY_TRACK_MODIFICATIONS=False))


db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = LoginManager(app)


app.app_context().push()

from bagel import models, routes

app.run(debug=True)
