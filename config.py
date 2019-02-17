import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # location of application's database is from SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')

    # this is set to False to disable a feature of Flask-SQLAlchemy that we don't need
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # sending errors by email - below are details to the configuration file
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None   #boolean flag to enable encrypted connections
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSOWRD')
    ADMINS = ['contact@oskarro.com']        # list of the email addresses that will receive error reports


