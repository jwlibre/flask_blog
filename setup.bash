#!/bin/bash

# set up environment variables for our Flask app.
# This is mandatory if running the app using the command
# $ flask run
# which is advantageous in giving us access to the Flask debugger command line.

# alternatively, use...
# if __name__ == '__main__':
#     app.run(debug=True)
# at the bottom of the Flask app code, and run the app using
# $ python app_name.py

# point Flask to our app
export FLASK_APP=run.py

# setup the Flask server in debug mode to allow us to make changes to the app without having to restart the server
export FLASK_DEBUG=1
