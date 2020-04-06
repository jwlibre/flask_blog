import os

# Setting up config as a class allows us to run multiple instances of the app with different configs
# (i.e. one for development, one for test, one for production, etc...)

class Config:
    # Specify where the database will be
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')  # /// implies relative to current location

    # secret key is for security purposes
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # setup the mail server
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')