from typing import Dict, Any

from .utils import get


class MixerCache:
    users: Dict[int, Any]
    messages: Dict[int, Any]

    def __init__(self, ws):
        self._ws = ws
        self._client = ws.client
    
    def update_user(self, data: Dict[str, Any]):
        ...

    def update_message(self, data: Dict[str, Any]):
        ...
