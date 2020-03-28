from flask import render_template, url_for, flash, redirect, request
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post
from flaskblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image

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

def save_picture(form_picture):
    # rename the file to a random hex string using secrets
    random_hex = secrets.token_hex(8) # 8 bytes long
    # extract extension
    _, f_ext = os.path.splitext(form_picture.filename) # underscore convention here is to represent variable that is not used in subsequent code
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    # scale down image to save space on filesystem, and to make website faster
    output_size = (100, 100)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            # set the user's profile picture, and add it to the database
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
