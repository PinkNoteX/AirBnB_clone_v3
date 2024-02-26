#!/usr/bin/python3
""" web app """
from flask import Flask, jsonify, make_response, Blueprint
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def not_found(e):
    """ 404 error """
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def teardown_app(e):
    """ teardown app """
    storage.close()


if __name__ == '__main__':
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', '5000'), threaded=True)
