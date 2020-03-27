from flask import render_template, url_for, flash, redirect
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flaskblog import app

# flaskblog is the package name.
# importing from flaskblog == importing from __init__.py
# importing from flaskblog.module == importing from one of the modules within flaskblog

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