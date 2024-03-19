"""
main entry point for example framelib flask app
"""

import json
from flask import Flask, url_for, jsonify, request
from framelib import frame, message, validate_message_or_mock_vercel, transaction

from .constant import ABI_WETH, CHAIN_ID, ADDRESS_WETH, IM_WETH

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
        image=IM_WETH,
        aspect_ratio='1:1',
        button1='deposit()',
        button1_action='tx',
        button1_target=url_for('tx_deposit', _external=True, value=f'{int(0.01e18):d}'),
        button2='withdraw()',
        button2_action='tx',
        button2_target=url_for('tx_withdraw', _external=True, value=f'{int(0.01e18):d}'),
        post_url=url_for('home', _external=True)
    )


@app.route('/tx/deposit', methods=['GET', 'POST'])
def tx_deposit():
    value = request.args.get('value')
    if value is None:
        raise ValueError
    abi = json.loads(ABI_WETH)
    return transaction(CHAIN_ID, ADDRESS_WETH, abi, value, 'deposit()')


@app.route('/tx/withdraw', methods=['GET', 'POST'])
def tx_withdraw():
    value = request.args.get('value')
    if value is None:
        raise ValueError
    abi = json.loads(ABI_WETH)
    return transaction(CHAIN_ID, ADDRESS_WETH, abi, value, 'withdraw(uint256)')
