import secrets
import os
from PIL import Image
from flask import url_for
from flask_mail import Message
from flaskblog import app, mail


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
