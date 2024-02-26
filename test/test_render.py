"""
test cases for frame rendering
"""

# lib
import time
import pytest
from flask import Flask

# src
from framelib import render_frame

app = Flask(__name__)


class TestRenderFrame(object):

    def test_one_button(self):
        with app.app_context():
            r = render_frame(button1='click')
            assert r.status_code == 200
            assert b'<meta property="fc:frame:button:1" content="click"/>' in r.data
            assert b'<meta property="fc:frame:button:2"' not in r.data

    def test_multiple_buttons(self):
        with app.app_context():
            r = render_frame(image='https://website.com/im.png', button1='click', button2='other', button3='back')
            assert r.status_code == 200
            assert b'<meta property="fc:frame:button:1" content="click"/>' in r.data
            assert b'<meta property="fc:frame:button:2" content="other"/>' in r.data
            assert b'<meta property="fc:frame:button:3" content="back"/>' in r.data
            assert b'<meta property="fc:frame:button:4"' not in r.data
            assert b'<meta property="fc:frame:image" content="https://website.com/im.png"/>' in r.data
