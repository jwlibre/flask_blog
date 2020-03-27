from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# ORM= Object-Relational Mapper - allows you to integrate relational database in an object-oriented way
# SQLAlchemy is an example of one of these.
# SQLAlchemy allows you to switch between different databases without having to change your Python code.
# we will use e.g. SQLLite for testing/development and PostGres for deployment

# Specify where the database will be
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # /// implies relative to current location

# secret key is for security purposes
app.config['SECRET_KEY'] = 'adf84588937c8f061e80fd21ba30d3bc'

# create the actual database
db = SQLAlchemy(app)


class User(db.Model):
    # creates a table with name 'user' (note lowercase!)
    # columns for table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False) # max length of string specified in validation
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') # we will hash each image to 20 characters
    password = db.Column(db.String(60), nullable=False) # pwds hashed to 60 chars
    posts = db.relationship('Post', backref='author', lazy=True)
    # posts is NOT a column - posts runs a query on the post table.
    # lazy refers to SQLAlchemy loading data from database:
    # lazy=True - gets all posts relating to the author at once.
    # backref allows us to access the author who created the post via the post table, by calling
    # post.author, even though 'author' is not defined as an attribute in the post table.

    def __repr__(self): # magic method to define how the object will be printed out
        return f"User('{self.username}, {self.email}, {self.image_file}')"


class Post(db.Model):
    # creates a table with name 'post' (note lowercase!)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) # max length of string specified in validation
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # don't use parentheses as we want to just pass the function, not call it
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}, {self.date_posted}')"


# sample result from a database call
posts = [
    {
        'author': 'JerBear',
        'title': 'blog post one',
        'content': 'first blog post content',
        'date_posted': 'January 20, 2020'
    },
    {
        'author': 'Margaret',
        'title': 'blog post two',
        'content': 'second blog post content',
        'date_posted': 'February 20, 2020'
    }

]

@app.route('/')
@app.route('/home') # add multiple decorators to allow the same function to be accessed via multiple routes
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Registration successful for {form.username.data}!', 'success')
        # redirect to homepage if successful registration
        return redirect(url_for('home')) # NAME OF THE FUNCTION FOR THAT ROUTE
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
            # danger = red alerting bootstrap class
    return render_template('login.html', title='Login', form=form)

# this conditional is only true if we run this script directly with Python - i.e. not calling it from another module
if __name__ == '__main__':
    app.run(debug=True)
