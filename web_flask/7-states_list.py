#!/usr/bin/python3
"""A simple flask server that uses sqlachemy"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown(request):
    storage.close()


@app.route('/states_list')
def states_view():
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


if __name__ == '__main__':
    app.run()
