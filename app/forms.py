from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class SignUpForm(FlaskForm):
    first_name = StringField('first_name', [DataRequired()])
    last_name = StringField('first_name', [DataRequired()])
    username = StringField('Username', [DataRequired()])
    email = StringField("Email", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    confirm_password = PasswordField("Confirm your password", [DataRequired(), EqualTo('password')])
    submit = SubmitField()


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField("Sign-In")

