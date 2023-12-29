#!/usr/bin/python3
"""A simple flask server that uses SQLAlchemy to display states"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes a db session"""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_view():
    """Renders a list of states"""
    states = storage.all(State)
    return render_template('7-states_list.html',
                           states=states.values())


if __name__ == "__main__":
    app.run()
