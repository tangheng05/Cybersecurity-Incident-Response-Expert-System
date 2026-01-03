from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=3, max=80)],
        render_kw={'placeholder': 'Enter username'}
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()],
        render_kw={'placeholder': 'Enter password'}
    )
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
