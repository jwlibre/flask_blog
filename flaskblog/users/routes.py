from flask import Blueprint, flash, redirect, url_for, render_template, request
from flask_login import current_user, login_required, login_user, logout_user
from flaskblog.models import User, Post
from flaskblog import db, bcrypt
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, ResetPasswordForm, RequestResetForm
from flaskblog.users.utils import save_picture, send_reset_email



users = Blueprint('users', __name__)


@users.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # hash the password
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        # redirect to homepage if successful registration
        flash(f'Registration successful for {form.username.data}! You are now able to log in.', 'success')
        return redirect(url_for('users.login')) # NAME OF THE FUNCTION FOR THAT ROUTE
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # log them in using flask_login extension
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') # returns None if 'next' parameter not present in URL
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
            # next_page = '/account', therefore we don't use url_for(next_page), as the / already means it's a url
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
            # danger = red alerting bootstrap class
    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)



@users.route('/home/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)  # sets default page to 1, and throws error if not an integer
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=3, page=page)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        # find the user corresponding to the submitted email
        user = User.query.filter_by(email=form.email.data).first()
        # send this user a reset password link by email
        send_reset_email(user)
        flash('An email has been sent with instructions on how to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form, legend='Reset Password')


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):  #i.e. reset the password with the reset token
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # hash the password
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        # redirect to homepage if successful registration
        flash(f'Your password has been reset. You are now able to log in.', 'success')
        return redirect(url_for('users.login'))  # NAME OF THE FUNCTION FOR THAT ROUTE
    return render_template('reset_token.html', title='Reset Password', form=form, legend='Reset Password')