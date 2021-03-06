import os
from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post, Visit


class UserModelCase(unittest.TestCase):

    # method that the unit testing framework executes before each test respectively
    # changing the application config to sqlite:// prevent tests from using the database that is used in development
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    # method that the unit testing framework executes after each test respectively
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # test that exercise the password hashing
    def test_password_hashing(self):
        u = User(username='oskar')
        u.set_password('1234')
        self.assertFalse(u.check_password('1111'))
        self.assertTrue(u.check_password('1234'))

    # test that exercise the the follow option
    def test_follow(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # create four users
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(body="post from john", author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from susan", author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from mary", author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from david", author=u4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u3)  # susan follows mary
        u3.follow(u4)  # mary follows david
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

    def test_follow_visits(self):
        # create four user
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four visits
        now = datetime.utcnow()
        v1 = Visit(body="visit from john", author=u1,
                   timestamp=now+timedelta(seconds=1))
        v2 = Visit(body="visit from susan", author=u2,
                   timestamp=now+timedelta(seconds=4))
        v3 = Visit(body="visit from mary", author=u3,
                   timestamp=now+timedelta(seconds=3))
        v4 = Visit(body="visit from david", author=u4,
                   timestamp=now+timedelta(seconds=2))
        db.session.add_all([v1, v2, v3, v4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u3)  # susan follows mary
        u3.follow(u4)  # mary follows david
        db.session.commit()

        # check the followed visits of each user
        f1 = u1.followed_visits().all()
        f2 = u2.followed_visits().all()
        f3 = u3.followed_visits().all()
        f4 = u4.followed_visits().all()
        self.assertEqual(f1, [v2, v4, v1])
        self.assertEqual(f2, [v2, v3])
        self.assertEqual(f3, [v3, v4])
        self.assertEqual(f4, [v4])




if __name__ == '__main__':
    unittest.main(verbosity=2)
