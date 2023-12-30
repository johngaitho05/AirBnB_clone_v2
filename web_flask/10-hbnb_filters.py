#!/usr/bin/python3
"""A simple flask server with a list view and a detail view of states"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes a db session"""
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def filters_view():
    """Renders a list of states as well as a list of
    cities for a given state"""
    states = storage.all(State)
    amenities = storage.all(Amenity)
    return render_template('10-hbnb_filters.html',
                           states=states.values(),
                           amenities=amenities.values())


if __name__ == "__main__":
    app.run()
