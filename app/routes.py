from flask import render_template, flash, redirect, url_for
from flask_login import current_user, logout_user, login_user

from app import app
from app.forms import LoginForm
from app.models import User


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Oskar'}
    posts = [
        {
            'author': {'username': 'Gosia'},
            'body': 'I have made new chocolate cake'
        },
        {
            'author': {'username': 'Misio'},
            'body': 'This is my dinner, which i did today'
        }
    ]

    visits = [
        {
            'author': {'username': 'Oski'},
            'body': 'It was really great pleasure!'
        },
        {
            'author': {'username': 'Dosia'},
            'body': 'BMG is one of the best restaurant in Warsaw'
        },
    ]

    return render_template('index.html', title='Home', user=user, posts=posts, visits=visits)


@app.route('/login',  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)