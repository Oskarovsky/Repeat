from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import Config

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)    # object that represents the database

migrate = Migrate(app, db)  # object that represents migration engine

login = LoginManager(app)   # object for managing the user logged-in state

from app import routes, models