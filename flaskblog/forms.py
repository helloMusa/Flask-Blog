from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class RegistrationForm(FlaskForm):
	username = StringField('Username', 
							validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', 
						 validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', 
									 validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	# Check if user already exists
	def validate_username(self, username):
		# If there is a value, we get the first value. If there isn't, we get None.
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken. Please choose a different one.')

	# Check if email already exists
	def validate_email(self, email):
		# If there is a value, we get the first value. If there isn't, we get None.
		email = User.query.filter_by(email=email.data).first()
		if email:
			raise ValidationError('That email is already registered.')

class LoginForm(FlaskForm):
	email = StringField('Email', 
						 validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

	



