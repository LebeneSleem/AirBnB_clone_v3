#!/usr/bin/python3
'''Contains a Flask web application API.
'''
import os
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views


app = Flask(__name__)
app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
app_port = int(os.getenv('HBNB_API_PORT', '5000'))
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={'/*': {'origins': app_host}})


# Custom 404 error handler
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404

# App context teardown function
@app.teardown_appcontext
def teardown_flask(exception):
    storage.close()

if __name__ == '__main__':
    app.run(
        host=app_host,
        port=app_port,
        threaded=True
    )
