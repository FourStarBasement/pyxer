from typing import Dict, Any

from .utils import get
from .mappings import Channel, ChatMessage


class MixerCache:
    users: Dict[int, Any] = {} # TODO: have one base user object
    messages: Dict[str, ChatMessage] = {}
    channels: Dict[int, Channel] = {}

    def __init__(self, ws):
        self._ws = ws
        self._client = ws.client
    
    def update_user(self, data: Dict[str, Any]):
        ...

    def update_message(self, data: Dict[str, Any]):
        ...

    def get_channel(self, channel_id: int):
        return self.channels.get(channel_id, None)

    def set_channel(self, channel: Channel):
        self.channels[channel.id] = channel
