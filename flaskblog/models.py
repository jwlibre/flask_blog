from datetime import datetime
from flaskblog import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# flask_login used to manage user login sessions

# taken from documentation
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin): # inherit from the UserMixin class to give the required methods and attributes to user in order for load_user to work out of the box
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

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    # method doesn't actually do anything with the instance of this user,
    # so we need to declare that it's a static method
    # i.e. don't expect self as an argument
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

class Post(db.Model):
    # creates a table with name 'post' (note lowercase!)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) # max length of string specified in validation
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # don't use parentheses as we want to just pass the function, not call it
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}, {self.date_posted}')"
