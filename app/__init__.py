from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import Config
import logging
from logging.handlers import SMTPHandler

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)    # object that represents the database

migrate = Migrate(app, db)  # object that represents migration engine

login = LoginManager(app)   # object for managing the user logged-in state
login.login_view = 'login'  # function (or endpoint) name for the login view. this is the name to use in a url_for()

from app import routes, models, errors

# function for sending out emails on errors (it is only running without DEBUG MODE)
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIN_USE_TLS']:
            secure=()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='RepEAT Failure!',
            credentials=auth,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
