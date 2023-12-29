#!/usr/bin/python3
"""A simple flask server with a dynamic route"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return "HBNB"


@app.route('/c/<string:text>', strict_slashes=False)
def c_something(text):
    return "C {}".format(text.replace('_', ' '))


if __name__ == '__main__':
    app.run()
