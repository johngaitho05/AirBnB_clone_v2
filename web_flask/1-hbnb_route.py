#!/usr/bin/python3
"""A simple flask server with 2 routes"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return "HBNB"


if __name__ == '__main__':
    app.run()
