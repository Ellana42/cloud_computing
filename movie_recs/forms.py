from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from movie_recs.models import User

class SearchForm(FlaskForm):
    search_term = StringField("Movie Name", 
                              validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField("Search")

class ReviewForm(FlaskForm):
    rating = SelectField("Rating", choices=range(6), coerce=int)
    submit = SubmitField("Rate")

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
