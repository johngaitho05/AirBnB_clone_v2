#!/usr/bin/python3
"""A simple flask server with a list view and a detail view of states"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes a db session"""
    storage.close()


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states_view(id=None):
    """Renders a list of states as well as a list of
    cities for a given state"""
    if not id:
        states = storage.all(State)
        return render_template('9-states.html',
                               states=states.values())
    state_id = 'State.{}'.format(id)
    state = storage.all(State).get(state_id)
    return render_template('9-states.html',
                           state=state)


if __name__ == "__main__":
    app.run()
