from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login


# function that can be called to load a user given the ID
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    visits = db.relationship('Visit', backref='author', lazy='dynamic')
    image_file = db.Column(db.String(50), nullable=True, default='default.jpg')

    # this method tells how to print objects of this class, which is going to be useful for debugging
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    # password hashing logic - generating password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # password hashing logic - verification password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    food_type = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}'.format(self.body)


class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    food_type = db.Column(db.String(140))
    place = db.Column(db.String(140))
    rate = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Visit {}>'.format(self.body)
