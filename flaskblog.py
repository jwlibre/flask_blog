from flask import Flask, render_template, url_for
app = Flask(__name__)

# sample result from a database call
posts = [
    {
        'author': 'JerBear',
        'title': 'blog post one',
        'content': 'first blog post content',
        'date_posted': 'January 20, 2020'
    },
    {
        'author': 'Margaret',
        'title': 'blog post two',
        'content': 'second blog post content',
        'date_posted': 'February 20, 2020'
    }

]

@app.route('/')
@app.route('/home') # add multiple decorators to allow the same function to be accessed via multiple routes
def hello_world():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')


# this conditional is only true if we run this script directly with Python - i.e. not calling it from another module
if __name__ == '__main__':
    app.run(debug=True)
