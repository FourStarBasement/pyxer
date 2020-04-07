from typing import Dict, Optional, List
from yarl import URL
from aiohttp import ClientSession


class HTTPConfig:
    client_secret: str
    client_id: str
    access_token: str


class HTTPClient:
    def __init__(self):
        self.config = HTTPConfig()
        self.session = None

    async def init(self, client_secret: str, client_id: str):
        self.session = ClientSession()
        self.config.client_secret = client_secret
        self.config.client_id = client_id

    def update_token(self, access_token: str):
        self.config.access_token = access_token

    async def request(self, verb: str, endpoint: str, *, query: Optional[Dict[str, str]]=None, data: Optional[Dict[str, str]]=None, headers: Optional[Dict[str, str]]={}):
        url = URL.build(scheme="https", host="mixer.com", path=f"/api/v1/{endpoint}", query=query)

        if hasattr(self.config, 'access_token'):
            headers['Authorization'] = f'Bearer {self.config.access_token}'

        async with self.session.request(verb, url, json=data, headers=headers) as r:
            #data = await r.json() if r.headers['content-type'] == 'application/json' else await r.text(encoding='utf-8')

            if r.status != 204:
                return await r.json()

    def get_shortcode(self, scope: List[str]):
        scopes = " ".join(scope)
        data = {
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
            "scope": scopes
        }
        return self.request('POST', 'oauth/shortcode', data=data)

    def verify_shortcode(self, handle: str):
        return self.request('GET', f'oauth/shortcode/check/{handle}')

    def get_tokens(self, token: str):
        data = {
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
            "grant_type": "authorization_code",
            "code": token
        }
        return self.request('POST', 'oauth/token', data=data)

    def refresh_tokens(self, token: str):
        data = {
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": token
        }
        return self.request('POST', 'oauth/token', data=data)

    def get_current_user(self):
        return self.request('GET', 'users/current')

    def get_connection_info(self, channel_id: int):
        return self.request('GET', f'chats/{channel_id}')
