from flask import render_template, flash, redirect

from app import app
from app.forms import LoginForm


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
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)