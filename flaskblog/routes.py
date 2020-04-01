from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog.forms import (RegistrationForm, LoginForm, UpdateAccountForm, PostForm,
                             RequestResetForm, ResetPasswordForm)
from flaskblog.models import User, Post
from flaskblog import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image
from flask_mail import Message

# flaskblog is the package name.
# importing from flaskblog == importing from __init__.py
# importing from flaskblog.module == importing from one of the modules within flaskblog


@app.route('/')
@app.route('/home') # add multiple decorators to allow the same function to be accessed via multiple routes
def home():
    page = request.args.get('page', 1, type=int)  # sets default page to 1, and throws error if not an integer
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=3, page=page)
    return render_template('home.html', posts=posts)

# homepage is paginated
# access multiple pages via eg http://localhost:5000/home?page=3


@app.route('/home/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)  # sets default page to 1, and throws error if not an integer
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=3, page=page)
    return render_template('user_posts.html', posts=posts, user=user)

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


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created.','success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='Create Post')


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id) #i.e. if post with post_id doesn't exist return a 404 error
    return render_template('post.html', title=post.title, post=post)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)  # http code for forbidden route
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit() # no add needed as this is an update to the db entries
        flash('Post has been updated.', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@app.route('/post/<int:post_id>/delete', methods=['POST']) # i.e. only posts allowed as it can only be accessed via modal submit
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)  # http code for forbidden route
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.', 'success')
    return redirect(url_for('home'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='pirate.watermelon.cress@gmail.com',
                  recipients=[user.email])
    # _external flag is used to make sure the URL is a full URL, not a relative one.
    # ensure the text within triple quotes is tabbed back to the baseline as per below,
    # or else there will be ugly tabs in the email text.
    # use Jinja templates for more complex emails.
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
    
If you did not make this request, simply ignore this email and no changes will be made.
'''
    mail.send(msg)



@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        # find the user corresponding to the submitted email
        user = User.query.filter_by(email=form.email.data).first()
        # send this user a reset password link by email
        send_reset_email(user)
        flash('An email has been sent with instructions on how to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form, legend='Reset Password')


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):  #i.e. reset the password with the reset token
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # hash the password
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        # redirect to homepage if successful registration
        flash(f'Your password has been reset. You are now able to log in.', 'success')
        return redirect(url_for('login'))  # NAME OF THE FUNCTION FOR THAT ROUTE
    return render_template('reset_token.html', title='Reset Password', form=form, legend='Reset Password')