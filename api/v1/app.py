#!/usr/bin/python3
"""This module contain a flask application that deals with APIs"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    """Call storage.close to close a session and get another"""
    storage.close()

@app.errorhandler(404)
def handle404(error):
    """Handle error, 404"""
    return make_response(jsonify({ "error": "Not found" }), 404)



if __name__ == '__main__':
    import os
    host = os.getenv('HBNB_API_HOST') or '0.0.0.0'
    port = os.getenv('HBNB_API_PORT') or 5000
    app.run(host=host, port=port, threaded=True)
