from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, URL, ValidationError

class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(message="Username is required"),
            Length(min=2, max=15, message="Username must be between 2 and 20 characters")
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required"),
            Length(min=6, message="Password must be at least 6 characters long")
        ]
    )
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class DataForm(FlaskForm):
    homepage = StringField(
        'Homepage',
        validators=[
            DataRequired(message="Homepage URL is required"),
            URL(message="Please enter a valid URL (e.g. https://example.com)")
        ]
    )

    submit = SubmitField('Submit')