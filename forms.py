from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField #TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    uname = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    twofa = StringField('Phone', validators=[DataRequired(), Length(min=9, max=10)])
    pword = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])
    confirm_pword = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=5, max=20), EqualTo('pword')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    uname = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    twofa = StringField('Phone', validators=[DataRequired(), Length(min=9, max=10)])
    pword = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SpellForm(FlaskForm):
    inputtext = StringField('Input Text', validators=[DataRequired()])
    submit = SubmitField('Submit')