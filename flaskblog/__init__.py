# flaskblog is now a package
# this is where we initialise the application and bring together different components

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

from flaskblog import routes
# if we don't import the routes, the app won't work - app unable to find the routes and therefore render the templates
# imported at bottom of file to prevent circular imports
