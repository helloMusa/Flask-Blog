from flask import render_template, url_for, flash, redirect
from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post


posts = [
	{
		'author': 'Musa Ali',
		'title': 'Blog Post 1',
		'content': 'First post content',
		'date_posted': 'November 10th, 2019'
	},
	{
		'author': 'John Smith',
		'title': 'Blog Post 2',
		'content': 'Second post content',
		'date_posted': 'November 11th, 2019'
	}
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
	return render_template('about.html', title=about)


@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	# If account registered successfully, redirect to home page
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	# If login succesful, redirect to homepage
	if form.validate_on_submit():
		if form.email.data == 'admin@blog.com' and form.password.data == 'password':
			flash('You have been logged in!', 'success')
			return redirect(url_for('home'))
		else:
			flash('Login Unsuccesful. Please check username and password.', 'danger')

	return render_template('login.html', title='Login', form=form)

