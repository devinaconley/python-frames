"""
data models
"""

import datetime
from typing import Optional
from pydantic import BaseModel


# ---- frame message ----

class CastId(BaseModel):
    fid: int
    hash: str


class UntrustedData(BaseModel):
    fid: int
    url: str
    messageHash: str
    timestamp: int
    network: int
    buttonIndex: int
    inputText: Optional[str] = None
    state: Optional[str] = None
    castId: CastId


class TrustedData(BaseModel):
    messageBytes: str


class FrameMessage(BaseModel):
    untrustedData: UntrustedData
    trustedData: TrustedData


# ---- neynar ----

class Viewer(BaseModel):
    following: bool
    followed_by: bool


class Bio(BaseModel):
    text: str
    mentioned_profiles: Optional[list[str]] = []


class Profile(BaseModel):
    bio: Bio


class Interactor(BaseModel):
    object: str
    fid: int
    username: str
    display_name: str
    custody_address: Optional[str] = None
    pfp_url: str
    profile: Profile
    follower_count: int
    following_count: int
    verifications: list[str]
    active_status: str
    viewer_context: Optional[Viewer] = None


class Button(BaseModel):
    title: Optional[str] = None
    index: int
    action_type: Optional[str] = None


class Input(BaseModel):
    text: str


class State(BaseModel):
    serialized: str


class Transaction(BaseModel):
    hash: str


class ValidatedMessage(BaseModel):
    object: str
    interactor: Interactor
    tapped_button: Button
    input: Optional[Input] = None
    state: Optional[State] = None
    url: str
    cast: dict
    timestamp: datetime.datetime
    transaction: Optional[Transaction] = None


# ---- warpcast ----

class Pfp(BaseModel):
    url: str
    verified: bool


class WarpBio(BaseModel):
    text: str
    mentions: Optional[list[str]] = []
    channelMentions: Optional[list[str]] = []


class WarpLocation(BaseModel):
    placeId: str
    description: str


class WarpProfile(BaseModel):
    bio: WarpBio
    location: WarpLocation


class User(BaseModel):
    fid: int
    username: Optional[str] = None
    displayName: str
    pfp: Optional[Pfp] = None
    profile: WarpProfile
    followerCount: int
    followingCount: int
    activeOnFcNetwork: bool
