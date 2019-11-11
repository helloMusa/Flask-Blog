from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required


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
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = RegistrationForm()

	# If account registered successfully, redirect to login page
	if form.validate_on_submit():
		# Hash user's password
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)

		# Add and commit user's info to databse
		db.session.add(user)
		db.session.commit()

		flash(f'Your account has been created! You are now able to login.', 'success')
		return redirect(url_for('login'))

	return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = LoginForm()
	# If login succesful, redirect to homepage
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()

		# Compare database password with password entered in form
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			# Log user in
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))

		else:
			flash('Login Unsuccesful. Please check email and password.', 'danger')

	return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))


@app.route("/account")
@login_required # Requires user to be logged in to view Account page
def account():
	return render_template('account.html', title='Account')
