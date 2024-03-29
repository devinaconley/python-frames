"""
main entry point for example framelib flask app
"""
import os
import time
from flask import Flask, url_for, jsonify
from framelib import frame, message, validate_message_or_mock_vercel

app = Flask(__name__)


@app.errorhandler(ValueError)
def handle_invalid_usage(e):
    print(f'error: {e}')
    response = jsonify({'status_code': 403, 'message': str(e)})
    response.status_code = 403
    return response


@app.route('/', methods=['GET', 'POST'])
def home():
    # initial frame
    return frame(
        image=_github_preview_image(),
        button1='hello \U0001F44B',
        post_url=url_for('second_page', _external=True),
        button2='github',
        button2_action='link',
        button2_target='https://github.com/devinaconley/python-frames'
    )


@app.route('/page2', methods=['POST'])
def second_page():
    # parse frame message
    msg = message()
    print(f'received frame message: {msg}')

    # validate frame message with neynar
    api_key = os.getenv('NEYNAR_KEY')
    msg_val = validate_message_or_mock_vercel(msg, api_key)
    print(f'validated frame message, fid: {msg_val.interactor.fid}, button: {msg_val.tapped_button}')

    return frame(
        image=_github_preview_image(),
        button1='back \U0001F519',
        post_url=url_for('home', _external=True),
        input_text=f'hello {msg_val.interactor.username}!',
        button2='github',
        button2_action='link',
        button2_target='https://github.com/devinaconley/python-frames'
    )


def _github_preview_image() -> str:
    hour = int((time.time() // 3600) * 3600)  # github throttles if you invalidate image cache too much
    return f'https://opengraph.githubassets.com/{hour}/devinaconley/python-frames'
