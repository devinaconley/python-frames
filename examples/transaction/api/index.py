"""
main entry point for example framelib flask app
"""

import json
from flask import Flask, url_for, jsonify, request
from framelib import frame, message, transaction
from eth_utils import to_wei

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
        button1_target=url_for('tx_deposit', _external=True, value=to_wei(0.01, 'ether')),
        button2='withdraw()',
        button2_action='tx',
        button2_target=url_for('tx_withdraw', _external=True, value=to_wei(0.01, 'ether')),
        input_text='WETH amount',
        post_url=url_for('home', _external=True),
        max_age=3600
    )


@app.route('/tx/deposit', methods=['GET', 'POST'])
def tx_deposit():
    # get amount from input field or query param
    try:
        msg = message()
        value = str(to_wei(float(msg.untrustedData.inputText), 'ether'))
    except:
        value = request.args.get('value')
    if value is None:
        raise ValueError('deposit amount missing')

    # transaction response
    abi = json.loads(ABI_WETH)
    return transaction(CHAIN_ID, ADDRESS_WETH, abi, value=value, function_signature='deposit()')


@app.route('/tx/withdraw', methods=['GET', 'POST'])
def tx_withdraw():
    # get amount from input field or query param
    try:
        msg = message()
        value = to_wei(float(msg.untrustedData.inputText), 'ether')
    except:
        value = int(request.args.get('value'))
    if value is None:
        raise ValueError('withdraw amount missing')

    # transaction response
    abi = json.loads(ABI_WETH)
    return transaction(CHAIN_ID, ADDRESS_WETH, abi, function_signature='withdraw(uint256)', function_arguments=[value])
