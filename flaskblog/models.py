from datetime import datetime
from flaskblog import db


class User(db.Model):
    # creates a table with name 'user' (note lowercase!)
    # columns for table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False) # max length of string specified in validation
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') # we will hash each image to 20 characters
    password = db.Column(db.String(60), nullable=False) # pwds hashed to 60 chars
    posts = db.relationship('Post', backref='author', lazy=True)
    # posts is NOT a column - posts runs a query on the post table.
    # lazy refers to SQLAlchemy loading data from database:
    # lazy=True - gets all posts relating to the author at once.
    # backref allows us to access the author who created the post via the post table, by calling
    # post.author, even though 'author' is not defined as an attribute in the post table.

    def __repr__(self): # magic method to define how the object will be printed out
        return f"User('{self.username}, {self.email}, {self.image_file}')"


class Post(db.Model):
    # creates a table with name 'post' (note lowercase!)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) # max length of string specified in validation
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # don't use parentheses as we want to just pass the function, not call it
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}, {self.date_posted}')"
