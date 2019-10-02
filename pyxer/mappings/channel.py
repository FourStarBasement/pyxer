from dataclasses import dataclass
from .base import Timestamped, Resource

@dataclass
class Channel(Timestamped):
    id: int
    userId: int
    token: str
    online: bool
    featured: bool
    featureLevel: int
    partnered: bool
    suspended: bool
    name: str
    audience: str
    viewersTotal: int
    viewersCurrent: int
    numFollowers: int
    description: str
    interactive: bool
    ftl: int
    hasVod: bool
    badgeId: int
    bannerUrl: str
    hosteeId: int
    hasTranscodes: bool
    vodsEnabled: bool

    interactiveGameId: int = None
    languageId: str = None
    coverId: int = None
    thumbnailId: int = None
    typeId: int = None
    transcodingProfileId: int = None
    costreamId: str = None

@dataclass
class ChannelAdvanced(Channel):
    type: dict = None
    user: dict = None

@dataclass
class ExpandedChannel(ChannelAdvanced):
    preferences: dict = None
    thumbnail: Resource = None
    cover: Resource = None
    badge: Resource = None
