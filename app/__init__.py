from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_bootstrap import Bootstrap

import os
from config import Config
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)    # object that represents the database
migrate = Migrate(app, db)  # object that represents migration engine

login = LoginManager(app)   # object for managing the user logged-in state
login.login_view = 'login'  # function (or endpoint) name for the login view. this is the name to use in a url_for()

moment = Moment(app)    # object for time and data rendering

bootstrap = Bootstrap   # object which provides a ready to use base template that has the bootstrap framework installed

mail = Mail(app)    # instance of email object

from app import routes, models, errors


if not app.debug:
    # method for sending out emails on errors (it is only running without DEBUG MODE)
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure=()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='RepEAT Failure!',
            credentials=auth,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    # method for enabling a file based log (it is only running without DEBUG MODE)
    # it's writing the log file with name 'repeat.log' in a logs directory (file is create if doesn't already exist)
    if not os.path.exists('logs'):
        os.mkdir('logs')
    # limiting the size of the log file to 10KB and number of keeping last log files to 10
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    # custom formatting the log messages (included: timestamp, logging level, message, source file, line number)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('RepEAT startup')


