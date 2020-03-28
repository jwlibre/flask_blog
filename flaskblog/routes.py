from flask import render_template, url_for, flash, redirect, request
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flaskblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # hash the password
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        # redirect to homepage if successful registration
        flash(f'Registration successful for {form.username.data}! You are now able to log in.', 'success')
        return redirect(url_for('login')) # NAME OF THE FUNCTION FOR THAT ROUTE
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # log them in using flask_login extension
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') # returns None if 'next' parameter not present in URL
            return redirect(next_page) if next_page else redirect(url_for('home'))
            # next_page = '/account', therefore we don't use url_for(next_page), as the / already means it's a url
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
            # danger = red alerting bootstrap class
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')