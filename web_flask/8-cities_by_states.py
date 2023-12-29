#!/usr/bin/python3
"""A simple flask server that uses SQLAlchemy To display cities by states"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes a db session"""
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def states_view():
    """Renders a list of cities grouped by states"""
    states = storage.all(State)
    return render_template('8-cities_by_states.html',
                           states=states.values())


if __name__ == "__main__":
    app.run()
