"""
test cases for frame transaction logic
"""

# lib
import json
import pytest
from flask import Flask

# src
from framelib import transaction

# constants
ABI_WETH = '[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"src","type":"address"},{"indexed":true,"internalType":"address","name":"guy","type":"address"},{"indexed":false,"internalType":"uint256","name":"wad","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"dst","type":"address"},{"indexed":false,"internalType":"uint256","name":"wad","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"src","type":"address"},{"indexed":true,"internalType":"address","name":"dst","type":"address"},{"indexed":false,"internalType":"uint256","name":"wad","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"src","type":"address"},{"indexed":false,"internalType":"uint256","name":"wad","type":"uint256"}],"name":"Withdrawal","type":"event"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"guy","type":"address"},{"internalType":"uint256","name":"wad","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"deposit","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"dst","type":"address"},{"internalType":"uint256","name":"wad","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"src","type":"address"},{"internalType":"address","name":"dst","type":"address"},{"internalType":"uint256","name":"wad","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"wad","type":"uint256"}],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'

app = Flask(__name__)


class TestTransaction(object):

    def test_deposit(self):
        abi = json.loads(ABI_WETH)
        with app.app_context():
            res = transaction(8453, '0x4200000000000000000000000000000000000006', abi,
                              value='50000000000000000', function_signature='deposit()')

            assert res.status_code == 200
            assert res.json['chainId'] == 'eip155:8453'
            assert res.json['method'] == 'eth_sendTransaction'
            assert res.json['params']['abi'] == abi
            assert res.json['params']['to'] == '0x4200000000000000000000000000000000000006'
            assert res.json['params']['value'] == '50000000000000000'
            assert res.json['params']['data'] == '0xd0e30db0'  # function selector

    def test_withdraw(self):
        abi = json.loads(ABI_WETH)
        with app.app_context():
            res = transaction(8453, '0x4200000000000000000000000000000000000006', abi,
                              function_signature='withdraw(uint256)', function_arguments=[int(123e18)])

            assert res.status_code == 200
            assert res.json['chainId'] == 'eip155:8453'
            assert res.json['method'] == 'eth_sendTransaction'
            assert res.json['params']['abi'] == abi
            assert res.json['params']['to'] == '0x4200000000000000000000000000000000000006'
            assert 'value' not in res.json['params']
            assert res.json['params']['data'] \
                   == '0x2e1a7d4d000000000000000000000000000000000000000000000006aaf7c8516d0c0000'  # function selector + encoded arg data
