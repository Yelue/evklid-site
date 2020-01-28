#module with flask forms. Register form and login form

from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, TextAreaField,\
					StringField, PasswordField,\
					DateField,SubmitField,validators

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[validators.Email(),validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(Form):
	email = StringField('Email',  validators=[validators.Email(),validators.Length(min=6,max=60)])
	password = PasswordField('Password',[validators.DataRequired(),
										validators.EqualTo('confirm',
											message='Passwords do not match')])
	first_name = StringField('First Name',[validators.Length(max=100)])
	second_name = StringField('Second Name',[validators.Length(max=100)])
	birthday = DateField('Birhday',format='%d-%m-%Y',validators=(validators.Optional(),))
	confirm = PasswordField('Confirm Password')

