"""
methods for frame rendering and message handling
"""

# lib
import json
from importlib import resources
from typing import Literal
from flask import render_template_string, request, make_response, jsonify, Response

# src
from .models import FrameMessage, FrameError

# enum types
ButtonActions = Literal['post', 'post_redirect', 'mint', 'link', 'tx']
AspectRatio = Literal['1.91:1', '1:1']


def frame(
        title: str = None,
        image: str = None,
        aspect_ratio: AspectRatio = None,
        content: str = None,
        post_url: str = None,
        button1: str = None,
        button1_action: ButtonActions = None,
        button1_target: str = None,
        button2: str = None,
        button2_action: ButtonActions = None,
        button2_target: str = None,
        button3: str = None,
        button3_action: ButtonActions = None,
        button3_target: str = None,
        button4: str = None,
        button4_action: ButtonActions = None,
        button4_target: str = None,
        input_text: str = None,
        state: str = None,
        max_age: int = None
) -> Response:
    # setup context
    # note: we do this because jinja treats None as a defined value
    ctx = {k: v for k, v in locals().items() if v is not None}

    # load template from module data
    pth = resources.files('framelib') / 'templates' / 'frame.html'
    with open(str(pth), 'r') as f:
        src = f.read()

    # render frame template
    html = render_template_string(src, **ctx)

    # response
    res = make_response(html)
    res.status_code = 200
    if max_age is not None:
        res.cache_control.max_age = max_age
    return res


def message() -> FrameMessage:
    # parse action message
    body = json.loads(request.data)
    msg = FrameMessage(**body)
    return msg


def error(text: str, status: int = 400) -> Response:
    if len(text) > 90:
        print('warning: error message exceeds 90 characters')
    e = FrameError(message=text)
    res = jsonify(e.model_dump())
    res.status_code = status
    return res
