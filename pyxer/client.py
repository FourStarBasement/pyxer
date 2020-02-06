from typing import List, Dict, Any
import asyncio
from webbrowser import open_new

from .http import HTTPClient
from .ws import WebSocketClient
from .oauth import OAuthHandler
from .utils import as_go_link


class MixerClient:
    scopes: List[str]
    http: HTTPClient
    oauth: OAuthHandler
    current_user: Dict[str, Any]
    ws: WebSocketClient

    def __init__(self, scopes: List[str]):
        self.scopes = scopes
        self.http = HTTPClient()

    async def start(self, client_secret: str, client_id: str):
        await self.http.init(client_secret, client_id)

        data = await self.http.get_shortcode(self.scopes)

        handle = data["handle"]

        code = data["code"]
        url = as_go_link(code)
        open_new(url)

        access_token, refresh_token = await self._wait_for_auth(handle)

        self.oauth = OAuthHandler(self.http, access_token, refresh_token)

        data = await self.http.get_current_user()

        self.current_user = data

        channel_id = data['channel']['id']
        user_id = data['channel']['userId']

        data = await self.http.get_connection_info(channel_id)

        self.ws = WebSocketClient(data['endpoints'][0])

        await self.ws.connect(channel_id, user_id, self.http.config.access_token, data['authkey'])

    def run(self, client_secret: str, client_id: str):
        asyncio.run(self.start(client_secret, client_id))

    async def _wait_for_auth(self, handle: str):
        while True:
            response = await self.http.verify_shortcode(handle)

            try:
                auth = response["code"]
            except TypeError:
                await asyncio.sleep(3)
            else:
                break

        tokens = await self.http.get_tokens(auth)

        return tokens["access_token"], tokens["refresh_token"]
            
