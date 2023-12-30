#!/usr/bin/python3
"""A simple flask server with a list view and a detail view of states"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.user import User

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes a db session"""
    storage.close()


@app.route('/hbnb', strict_slashes=False)
def hbnb_view():
    """Renders a list of states as well as a list of
    cities for a given state"""
    states = storage.all(State)
    amenities = storage.all(Amenity)
    places = storage.all(Place)
    users = {user.id: user for user in storage.all(User).values()}
    return render_template('100-hbnb.html',
                           states=states.values(),
                           amenities=amenities.values(),
                           places=places.values(),
                           users=users)


if __name__ == "__main__":
    app.run()
