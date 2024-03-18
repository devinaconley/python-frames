"""
methods to call neynar api
"""
import os

import requests

from .models import FrameMessage, ValidatedMessage, Interactor, NeynarProfile, NeynarBio, NeynarButton, NeynarInput, \
    NeynarState, NeynarTransaction


def get_frame_action(msg: str, api_key: str) -> ValidatedMessage:
    if not api_key:
        raise ValueError('neynar api key not set')
    url = 'https://api.neynar.com/v2/farcaster/frame/validate'
    body = {
        'cast_reaction_context': False,  # TODO
        'follow_context': False,
        'signer_context': False,
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

    if msg.untrustedData.state is not None and msg.untrustedData.state != action.state.serialized:
        raise ValueError(f'state does not match: {msg.untrustedData.state} {action.state.serialized}')

    return action


def validate_message_or_mock(msg: FrameMessage, api_key: str, mock: bool = False) -> ValidatedMessage:
    if mock:
        # mock
        # TODO option to populate with warpcast profile
        return ValidatedMessage(
            object='validated_frame_action',
            interactor=Interactor(
                object='user',
                fid=msg.untrustedData.fid,
                username=f'username {msg.untrustedData.fid}',
                display_name=f'display name {msg.untrustedData.fid}',
                pfp_url='',
                profile=NeynarProfile(bio=NeynarBio(text='')),
                follower_count=0,
                following_count=0,
                verifications=['0x'],
                active_status='',
            ),
            tapped_button=NeynarButton(index=msg.untrustedData.buttonIndex),
            input=NeynarInput(text=msg.untrustedData.inputText or ''),  # TODO set model to None if missing
            state=NeynarState(serialized=msg.untrustedData.state or ''),
            transaction=NeynarTransaction(hash=msg.untrustedData.transactionId or ''),
            url=msg.untrustedData.url,
            timestamp=msg.untrustedData.timestamp,
            cast={}
        )

    return validate_message(msg, api_key)


def validate_message_or_mock_vercel(msg: FrameMessage, api_key: str) -> ValidatedMessage:
    vercel_env = os.getenv('VERCEL_ENV')
    return validate_message_or_mock(msg, api_key, vercel_env is None or vercel_env == 'development')
