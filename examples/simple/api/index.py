"""
main entry point for example framelib flask app
"""
import json
import time
from flask import Flask, render_template, url_for, request, make_response, jsonify
from framelib.models import FrameMessage

app = Flask(__name__)


class BadRequest(Exception):
    pass


@app.errorhandler(BadRequest)
def handle_invalid_usage(e):
    response = jsonify({'status_code': 403, 'message': str(e)})
    response.status_code = 403
    return response


@app.route('/', methods=['GET', 'POST'])
def home():
    return jsonify({'status_code': 200, 'message': 'hello world'})


@app.route('/page2', methods=['POST'])
def second_page():
    return jsonify({'status_code': 200, 'message': 'hello world, page 2'})
