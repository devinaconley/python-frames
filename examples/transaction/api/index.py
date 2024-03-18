"""
main entry point for example framelib flask app
"""

import json
from flask import Flask, url_for, jsonify, request
from framelib import frame, message, validate_message_or_mock_vercel, transaction

from .constant import ABI_WETH, CHAIN_ID, ADDRESS_WETH

app = Flask(__name__)


@app.errorhandler(ValueError)
def handle_invalid_usage(e):
    print(f'error: {e}')
    response = jsonify({'status_code': 403, 'message': str(e)})
    response.status_code = 403
    return response


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        msg = message()
        print(f'received frame message: {msg}')

    return frame(
        image='https://token-repository.dappradar.com/tokens?protocol=ethereum&contract=0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2&file=logo.png',
        aspect_ratio='1:1',
        button1='deposit()',
        button1_action='tx',
        button1_target=url_for('tx_deposit', _external=True),
        post_url=url_for('home', _external=True)
    )


@app.route('/tx/deposit', methods=['GET', 'POST'])
def tx_deposit():
    print(request.method)
    print(request.data)
    abi = json.loads(ABI_WETH)
    return transaction(CHAIN_ID, ADDRESS_WETH, abi, f'{int(0.01e18):d}', 'deposit()')
