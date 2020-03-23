from flask import Flask
app = Flask(__name__)


@app.route('/')
@app.route('/home') # add multiple decorators to allow the same function to be accessed via multiple routes
def hello_world():
    return '<h1>Homepage</h1>'

@app.route('/about')
def about():
    return '<h1>About</h1>'


# this conditional is only true if we run this script directly with Python - i.e. not calling it from another module
if __name__ == '__main__':
    app.run(debug=True)