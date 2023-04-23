#!/usr/bin/python3
"""
Starts a Flask web application
"""

from models import storage
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    """
    Display a HTML page with a list of States
    """
    states = storage.all('State')
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """
    Display a HTML page with the State and it's Cities
    """
    states = storage.all('State')
    for state in states.values():
        if state.id == id:
            return render_template('9-states.html', state=state, id=id)
    return render_template('9-states.html')


@app.teardown_appcontext
def teardown_db(exception):
    """Remove the current SQLAlchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
