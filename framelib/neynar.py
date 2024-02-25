"""
methods to call neynar api
"""
import os

import requests

from .models import FrameMessage, ValidatedMessage, Interactor, Profile, Bio, Button, Input


def get_frame_action(msg: str) -> (bool, ValidatedMessage):
    key = os.getenv('NEYNAR_KEY')
    url = 'https://api.neynar.com/v2/farcaster/frame/validate'
    body = {
        'cast_reaction_context': False,
        'follow_context': False,
        'message_bytes_in_hex': msg
    }
    headers = {
        'accept': 'application/json',
        'api_key': key,
        'content-type': 'application/json'
    }
    res = requests.post(url, json=body, headers=headers)

    body = res.json()
    if not body['valid']:
        return False, None

    print(body)
    action = ValidatedMessage(**body['action'])
    print(action)

    return True, action


def validate_message(msg: FrameMessage) -> (bool, ValidatedMessage):
    valid, action = get_frame_action(msg.trustedData.messageBytes)
    if not valid:
        return valid, action

    if msg.untrustedData.fid != action.interactor.fid:
        print(f'fid does not match: {msg.untrustedData.fid} {action.interactor.fid}')
        return False, action

    if msg.untrustedData.buttonIndex != action.tapped_button.index:
        print(f'button index does not match: {msg.untrustedData.buttonIndex} {action.tapped_button.index}')
        return False, action

    if msg.untrustedData.inputText is not None and msg.untrustedData.inputText != action.input.text:
        print(f'text input does not match: {msg.untrustedData.inputText} {action.input.text}')
        return False, action

    return valid, action


def validate_message_or_mock(msg: FrameMessage) -> (bool, ValidatedMessage):
    if os.getenv('VERCEL_ENV') is None:
        # mock
        return True, ValidatedMessage(
            object='validated_frame_action',
            interactor=Interactor(
                object='user',
                fid=msg.untrustedData.fid,
                username=f'username {msg.untrustedData.fid}',
                display_name=f'display name {msg.untrustedData.fid}',
                pfp_url='',
                profile=Profile(bio=Bio(text='')),
                follower_count=0,
                following_count=0,
                verifications=['0x'],
                active_status='',
            ),
            tapped_button=Button(index=msg.untrustedData.buttonIndex),
            input=Input(text=msg.untrustedData.inputText or ''),
            url=msg.untrustedData.url,
            cast={}
        )

    return validate_message(msg)
