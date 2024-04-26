"""
main entry point for example framelib flask app
"""
import os
import time
from flask import Flask, url_for, jsonify
from framelib import frame, message, validate_message_or_mock, validate_message_or_mock_neynar, error

app = Flask(__name__)


@app.errorhandler(ValueError)
def handle_invalid_usage(e):
    print(f'error: {e}')
    return error(text=str(e), status=403)


@app.route('/', methods=['GET', 'POST'])
def home():
    # initial frame
    return frame(
        image=_github_preview_image(),
        button1='hello \U0001F44B',
        post_url=url_for('second_page', _external=True),
        button2='do not press \U0001F6AB',
        button3='github',
        button3_action='link',
        button3_target='https://github.com/devinaconley/python-frames'
    )


@app.route('/page2', methods=['POST'])
def second_page():
    # parse frame message
    msg = message()
    print(f'received frame message: {msg}')

    # check input
    if msg.untrustedData.buttonIndex == 2:
        print('invalid button input')
        return error('wrong button!')  # popup message to user

    # validate frame message with neynar
    api_key = os.getenv('NEYNAR_KEY')
    msg_neynar = validate_message_or_mock_neynar(msg, api_key, mock=_vercel_local())
    print(f'validated frame message, fid: {msg_neynar.interactor.fid}, button: {msg_neynar.tapped_button}')

    # validate frame message with hub (alternative)
    # msg_hub = validate_message_or_mock(msg, 'https://nemes.farcaster.xyz:2281', mock=_vercel_local())
    # print(f'validated frame message hub, fid: {msg_hub.data.fid}, button: {msg_hub.data.frameActionBody.buttonIndex}')

    return frame(
        image=_github_preview_image(),
        button1='back \U0001F519',
        post_url=url_for('home', _external=True),
        input_text=f'hello {msg_neynar.interactor.username}!',
        button2='github',
        button2_action='link',
        button2_target='https://github.com/devinaconley/python-frames'
    )


def _github_preview_image() -> str:
    hour = int((time.time() // 3600) * 3600)  # github throttles if you invalidate image cache too much
    return f'https://opengraph.githubassets.com/{hour}/devinaconley/python-frames'


def _vercel_local() -> bool:
    vercel_env = os.getenv('VERCEL_ENV')
    return vercel_env is None or vercel_env == 'development'
