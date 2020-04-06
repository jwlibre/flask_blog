from flaskblog import create_app
# imports app from the __init__.py file within the flaskblog package

app = create_app()

# this conditional is only true if we run this script directly with Python - i.e. not calling it from another module
if __name__ == '__main__':
    app.run(debug=True)
