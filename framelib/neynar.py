"""
methods to call neynar api
"""
import os

import requests

from .models import FrameMessage, ValidatedMessage, Interactor, Profile, Bio, Button, Input


def get_frame_action(msg: str, api_key: str) -> ValidatedMessage:
    url = 'https://api.neynar.com/v2/farcaster/frame/validate'
    body = {
        'cast_reaction_context': False,  # TODO
        'follow_context': False,
        'message_bytes_in_hex': msg
    }
    headers = {
        'accept': 'application/json',
        'api_key': api_key,
        'content-type': 'application/json'
    }
    res = requests.post(url, json=body, headers=headers)

    body = res.json()
    if not body['valid']:
        raise ValueError('frame action message is invalid')

    action = ValidatedMessage(**body['action'])

    return action


def validate_message(msg: FrameMessage, api_key: str) -> ValidatedMessage:
    action = get_frame_action(msg.trustedData.messageBytes, api_key)

    if msg.untrustedData.fid != action.interactor.fid:
        raise ValueError(f'fid does not match: {msg.untrustedData.fid} {action.interactor.fid}')

    if msg.untrustedData.buttonIndex != action.tapped_button.index:
        raise ValueError(f'button index does not match: {msg.untrustedData.buttonIndex} {action.tapped_button.index}')

    if msg.untrustedData.inputText is not None and msg.untrustedData.inputText != action.input.text:
        raise ValueError(f'text input does not match: {msg.untrustedData.inputText} {action.input.text}')

    return action


def validate_message_or_mock(msg: FrameMessage, api_key: str, mock: bool = False) -> ValidatedMessage:
    if mock:
        # mock
        return ValidatedMessage(
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

    return validate_message(msg, api_key)


def validate_message_or_mock_vercel(msg: FrameMessage, api_key: str) -> (bool, ValidatedMessage):
    return validate_message_or_mock(msg, api_key, os.getenv('VERCEL_ENV') is None)
