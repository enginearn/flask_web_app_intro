from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignUpForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired('Please enter a username.'),
            Length(min=4, max=25)
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired('Please enter an email address.'),
            Email(),
            Length(min=6, max=40)
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired('Please enter a password.'),
            Length(min=6, max=40)
        ]
    )
    submit = SubmitField('Sign Up')
