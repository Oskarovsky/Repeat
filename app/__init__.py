from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)    # object that represents the database

migrate = Migrate(app, db)  # object that represents migration engine

from app import routes, models