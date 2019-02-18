from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login


# followers association table
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    visits = db.relationship('Visit', backref='author', lazy='dynamic')
    image_file = db.Column(db.String(50), nullable=True, default='default.jpg')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    '''
    # many-to-many relationship
    followed = db.relationship(
        'User',                 # the right side entity of the relationship (the left side entity is the parent class)
        secondary=followers,    # it configures the association table that is used for the relationship
        primaryjoin=(followers.c.follower_id == id),    # it indicates the condition that links the left side entity
        secondaryjoin=(followers.c.follower_id == id),  # it indicates the condition that links the right side entity
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic')
        '''

    # this method tells how to print objects of this class, which is going to be useful for debugging
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    # password hashing logic - generating password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # password hashing logic - verification password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # method for adding relationships
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    # method for removing relationships
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    # method for checking if a link between two users already exists
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    # method for obtaining posts from followed users
    def followed_posts(self):
        followed = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).\
            filter(followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    # method for obtaining visits from followed users
    def followed_visits(self):
        followed = Visit.query.join(followers, (followers.c.followed_id == Visit.user_id)).\
            filter(followers.c.follower_id == self.id)
        own = Visit.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Visit.timestamp.desc())


# function that can be called to load a user given the ID
@login.user_loader
def load_user(id):
    return User.query.get(int(id))





class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    food_type = db.Column(db.String(140))
    description = db.Column(db.String(3000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}'.format(self.body)


class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    food_type = db.Column(db.String(140))
    description = db.Column(db.String(3000))
    place = db.Column(db.String(140))
    rate = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Visit {}>'.format(self.body)
