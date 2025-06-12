import os
from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()

# Creates the app during instantiation
def create_app(debug=False):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'AKWNF1231082fksejfOSEHFOISEHF24142124124124124iesfhsoijsopdjf'
    app.debug = debug

    from .utils.database.database import database
    db = database()
    db.createTables(purge=True)

    socketio.init_app(app)

    with app.app_context():
        from . import routes
        return app
