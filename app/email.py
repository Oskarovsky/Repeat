from threading import Thread

from flask_mail import Message
from flask import render_template
from app import mail, app

# helper function that sends an email, which is basically a generic version of the shell
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


# function for sending a password reset email
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[RepEAT] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))

# function that running in a background thread
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
