# flaskblog is now a package
# this is where we initialise the application and bring together different components

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # pass in the function name of the route to tell the login manager
# where the login page is found
login_manager.login_message_category = 'info' # bootstrap category to make info message nicer

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

# setup the mail server
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
print(os.environ.get('EMAIL_USER'))
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

from flaskblog import routes
# if we don't import the routes, the app won't work - app unable to find the routes and therefore render the templates
# imported at bottom of file to prevent circular imports
