"""
methods to query farcaster data from the warpcast api
"""

import requests

from .models import User


def get_user(fid: int) -> User:
    res = requests.get('https://client.warpcast.com/v2/user', params={'fid': fid})
    return User(**res.json()['result']['user'])
