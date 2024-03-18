"""
test cases for frame rendering
"""

# lib
import time
import json
from urllib.parse import quote, unquote
import pytest
from flask import Flask

# src
from framelib import frame

app = Flask(__name__)


class TestRenderFrame(object):

    def test_one_button(self):
        with app.app_context():
            r = frame(button1='click')
            assert r.status_code == 200
            assert b'<meta property="fc:frame:button:1" content="click"/>' in r.data
            assert b'<meta property="fc:frame:button:2"' not in r.data

    def test_multiple_buttons(self):
        with app.app_context():
            r = frame(image='https://website.com/im.png', button1='click', button2='other', button3='back')
            assert r.status_code == 200
            assert b'<meta property="fc:frame:button:1" content="click"/>' in r.data
            assert b'<meta property="fc:frame:button:2" content="other"/>' in r.data
            assert b'<meta property="fc:frame:button:3" content="back"/>' in r.data
            assert b'<meta property="fc:frame:button:4"' not in r.data
            assert b'<meta property="fc:frame:image" content="https://website.com/im.png"/>' in r.data

    def test_aspect_ratio_default(self):
        with app.app_context():
            r = frame(image='https://website.com/im.png')
            assert r.status_code == 200
            assert b'<meta property="fc:frame:image" content="https://website.com/im.png"/>' in r.data
            assert b'<meta property="fc:frame:image:aspect_ratio"' not in r.data

    def test_aspect_ratio_1_1(self):
        with app.app_context():
            r = frame(image='https://website.com/im.png', aspect_ratio='1:1')
            assert r.status_code == 200
            assert b'<meta property="fc:frame:image" content="https://website.com/im.png"/>' in r.data
            assert b'<meta property="fc:frame:image:aspect_ratio" content="1:1"/>' in r.data

    def test_state(self):
        with app.app_context():
            s = quote(json.dumps({'app': 'state'}))
            r = frame(image='https://website.com/im.png', state=s)
            assert r.status_code == 200
            assert b'<meta property="fc:frame:image" content="https://website.com/im.png"/>' in r.data
            assert f'<meta property="fc:frame:state" content="{s}"/>'.encode('utf-8') in r.data

    def test_max_age_default(self):
        with app.app_context():
            r = frame(image='https://website.com/im.png')
            assert r.status_code == 200
            assert r.cache_control.max_age is None
            assert b'<meta property="fc:frame:image" content="https://website.com/im.png"/>' in r.data

    def test_max_age_short(self):
        with app.app_context():
            r = frame(image='https://website.com/im.png', max_age=60)
            assert r.status_code == 200
            assert r.cache_control.max_age == 60
            assert b'<meta property="fc:frame:image" content="https://website.com/im.png"/>' in r.data

    def test_max_age_zero(self):
        with app.app_context():
            r = frame(image='https://website.com/im.png', max_age=0)
            assert r.status_code == 200
            assert r.cache_control.max_age == 0
            assert b'<meta property="fc:frame:image" content="https://website.com/im.png"/>' in r.data
