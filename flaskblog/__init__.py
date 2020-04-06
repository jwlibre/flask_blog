# flaskblog is now a package, as it has an init file.
# this is where we initialise the application and bring together different components

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config


bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login' # pass in the function name of the route to tell the login manager
# where the login page is found
login_manager.login_message_category = 'info' # bootstrap category to make info message nicer

# ORM= Object-Relational Mapper - allows you to integrate relational database in an object-oriented way
# SQLAlchemy is an example of one of these.
# SQLAlchemy allows you to switch between different databases without having to change your Python code.
# we will use e.g. SQLLite for testing/development and PostGres for deployment


# create the actual database
db = SQLAlchemy()

mail = Mail()


# if we don't import the routes, the app won't work - app unable to find the routes and therefore render the templates
# imported at bottom of file to prevent circular imports

# Flask documentation says that we setup the externals EXTERNALLY to the create_app function
# so that the extension object does not initially get bound to the application - no application-specific state
# is stored on the extension object, so one extension object can be used for multiple apps.

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # extensions:
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # import the users blueprint and register it
    from flaskblog.users.routes import users
    app.register_blueprint(users)

    from flaskblog.posts.routes import posts
    app.register_blueprint(posts)

    from flaskblog.main.routes import main
    app.register_blueprint(main)

    return app
