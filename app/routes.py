import secrets
import os
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, logout_user, login_user, login_required
from werkzeug.urls import url_parse
from PIL import Image
from datetime import datetime

from app import app, db
from app.forms import LoginForm, RegistrationForm, UpdateForm, PostForm, VisitForm
from app.models import User, Post, Visit


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    if current_user.is_authenticated:
        posts = current_user.followed_posts().paginate(
            page, app.config['POSTS_PER_PAGE_INDEX'], False)
        visits = current_user.followed_visits().paginate(
            page, app.config['VISITS_PER_PAGE_INDEX'], False)
    else:
        posts = Post.query.paginate(
            page, app.config['POSTS_PER_PAGE_INDEX'], False)
        visits = Visit.query.paginate(
            page, app.config['VISITS_PER_PAGE_INDEX'], False)
    return render_template('index.html', title='Home Page', posts=posts.items, visits=visits.items)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        flash('You have been logged in!', 'success')
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



# function for saving users picture
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)  # method for splitting on two names fragments of file
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # resizing uploaded image
    output_size = (140, 140)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route('/user/<username>', methods=['GET', 'POST'])      # f.e. /user/oskarro   --> username=oskarro
@login_required
def user(username):
    form = UpdateForm()
    user = User.query.filter_by(username=username).first_or_404()
    # update users account
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user.image_file = picture_file
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('user', username=form.username.data, email=form.email.data))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE_USER'], False)
    visits = user.visits.order_by(Visit.timestamp.desc()).paginate(
        page, app.config['VISITS_PER_PAGE_USER'], False)
    return render_template('user.html', user=user, image_file=image_file,
                           form=form, posts=posts.items, visits=visits.items)



@app.route('/user/<username>/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    form = UpdateForm()
    user = User.query.filter_by(username=username).first_or_404()
    # if validate_on_submit() returns True, the data is copying from the form into the user object
    # and then it is writing the object to the database
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user.image_file = picture_file
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('user', username=form.username.data, email=form.email.data, about_me=form.about_me.data))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    return render_template('edit_profile.html', title='Edit Profile', form=form, image_file=image_file)



@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))



@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))



@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data, description=form.description.data, food_type=form.food_type.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('create_post.html', title='New Post', form=form)



@app.route('/visit/new', methods=['GET', 'POST'])
@login_required
def new_visit():
    form = VisitForm()
    if form.validate_on_submit():
        visit = Visit(body=form.body.data, food_type=form.food_type.data, description=form.description.data,
                      place=form.place.data, rate=form.rate.data, author=current_user)
        db.session.add(visit)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('create_visit.html', title='New Visit', form=form)



@app.route('/explore')
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
            page, app.config['POSTS_PER_PAGE_EXPLORE'], False)
    visits = Visit.query.order_by(Visit.timestamp.desc()).paginate(
            page, app.config['VISITS_PER_PAGE_EXPLORE'], False)
    return render_template('index.html', title='Explore', posts=posts.items, visits=visits.items)
