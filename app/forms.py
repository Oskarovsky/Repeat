from flask_login import current_user
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))



class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(_l('Repeat password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Register'))

    # function checks if entered username is not already in database
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_l('Please use a different username.'))

    # function checks if entered email address is not already in database
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_l('Please use a different email address.'))



class UpdateForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    picture = FileField(_l('Update Profile Picture'), validators=[FileAllowed(['jpg', 'png'])])
    about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Update'))


    # function checks if entered username is not already in database
    # it also compares entered new username with present username
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError(_l('Please use a different username.'))

    # function checks if entered email address is not already in database
    # it also compares entered new email with present username
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError(_l('Please use a different email address.'))



class PostForm(FlaskForm):
    body = StringField(_l('Title'), validators=[DataRequired()])
    description = TextAreaField(_l('Repeat about something'), validators=[DataRequired()])
    food_type = StringField(_l('Food type'), validators=[DataRequired()])
    submit = SubmitField(_l('Repeat!'))



class VisitForm(FlaskForm):
    body = StringField(_l('Name'), validators=[DataRequired()])
    food_type = StringField(_l('Food type'), validators=[DataRequired()])
    description = TextAreaField(_l('Repeat about place'), validators=[DataRequired()])
    place = StringField(_l('Place'), validators=[DataRequired()])
    rate = StringField(_l('Your rate'), validators=[DataRequired()])
    submit = SubmitField(_l('Repeat!'))



class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))



class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(_l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))