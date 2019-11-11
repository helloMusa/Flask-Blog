from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c7a90ad4a00c1e1e58863f6c7cbdd50c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	# Backref allows us to get user who created the post
	posts = db.relationship('Post', backref='author', lazy=True)

	# How the object will be printed
	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	# ID of user who authored the post
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		# One user can have many posts, one post can only have on author
		return f"Post('{self.title}', '{self.date_posted}')"


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


if __name__ == '__main__':
	app.run(debug=True)