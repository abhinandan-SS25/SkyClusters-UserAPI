from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[validators.DataRequired()])
    email = StringField('email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('password', validators=[validators.DataRequired()])
    confirm = PasswordField('confirm_password', validators=[validators.DataRequired()])
    
class LoginForm(FlaskForm):
    email = StringField('email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('password', validators=[validators.DataRequired()])