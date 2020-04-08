from typing import Dict, Optional, List
from yarl import URL
from aiohttp import ClientSession
from mappings.channel import Channel, ExpandedChannel


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

    async def request(self, verb: str, endpoint: str, *, query: Optional[Dict[str, str]]=None, data: Optional[Dict[str, str]]=None, headers: Optional[Dict[str, str]]={}, clazz=None):
        url = URL.build(scheme="https", host="mixer.com", path=f"/api/v1/{endpoint}", query=query)

        if hasattr(self.config, 'access_token'):
            headers['Authorization'] = f'Bearer {self.config.access_token}'

        async with self.session.request(verb, url, json=data, headers=headers) as r:
            data = await r.json() if r.headers['content-type'] == 'application/json' else await r.text(encoding='utf-8')

            if 300 > r.status >= 200:
                if clazz:
                    return clazz(**data)
                else:
                    return data

            if r.status == 429:
                retry_after = data['retry_after'] / 1000.0

                print(f"You are being ratelimited! Retrying request after {retry_after} seconds.")
                await asyncio.sleep(retry_after)
                await self.request(verb, endpoint, query=query, data=data, headers=headers, clazz=clazz)

                return

            if r.status == 403:
                raise Exception('Forbidden.')
            elif r.status == 404:
                raise Exception('Not Found.')

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

    def get_channel_id(self, username: str):
        '''
        Gets a single user's channel id

        Args:
            username (str): The username whos channel you want to get

        Returns:
            json: The id of the requested user
        '''
        return self.request('GET', f'/channels/{username}?fields=id')

    def get_connection_info(self, channel_id: int):
        '''
        Gets the info of the supplied channel

        Args:
            channel_id (str): The channel whos information you want to get

        Returns:
            json: The channels chatroom settings if authenticated
        '''
        return self.request('GET', f'chats/{channel_id}')

    def get_channel(self, channel_identifier: str):
        '''
        '''
        return self.request('GET', f'channels/{channel_identifier}', clazz=ExpandedChannel)

    def get_ingests(self):
        return self.request('GET', 'ingests')
