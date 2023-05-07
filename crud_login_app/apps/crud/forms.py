from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, length

class UserForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required'),
            length(min=4, max=20, message='Username must be between 4 and 20 characters')
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Email is required'),
            Email(message='Invalid email'),
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required'),
            length(min=4, max=20, message='Password must be between 4 and 20 characters')
        ]
    )
    submit = SubmitField('Submit')
