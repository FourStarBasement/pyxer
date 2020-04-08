from dataclasses import dataclass
from .base import Timestamped, Resource


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

    def __init__(self, *, client, data):
        super().__init__(client=client, data=data)
        self._parse_data(data)

    def _parse_data(self, data):
        self.id = data['id']
        self.user_id = data['userId'] # TODO: fetch and serialise
        self.token = data.get('token')
        self.online = data['online']
        self.featured = data['featured']
        self.feature_level = data['featureLevel']
        self.partnered = data['partnered']
        self.suspended = data['suspended']
        self.name = data['name']
        self.audience = data['audience']
        self.total_viewers = data['viewersTotal']
        self.current_viewers = data['viewersCurrent']
        self.followers = data['numFollowers']
        self.description = data['description']
        self.ftl = data['ftl']
        self.has_vod = data['hasVod']
        self.badge_id = data['badgeId']
        self.banner_url = data['bannerUrl']
        self.hosteeId = data['hosteeId']
        self.hasTranscodes = data['hasTranscodes']
        self.vodsEnabled = data['vodsEnabled']

# TODO: complete these classes

class ChannelAdvanced(Channel):
    type: dict = None
    user: dict = None


class ExpandedChannel(ChannelAdvanced):
    preferences: dict = None
    thumbnail: Resource = None
    cover: Resource = None
    badge: Resource = None
