from typing import List, Dict, Any
import asyncio
from webbrowser import open_new

from .http import HTTPClient
from .ws import WebSocketClient
from .scopes import Scopes
from .oauth import OAuthHandler
from .utils import as_go_link
from .event import Listener


class MixerClient:
    scopes: Scopes
    http: HTTPClient
    oauth: OAuthHandler
    current_user: Dict[str, Any]
    ws: WebSocketClient

    def __init__(self, *, scopes: Scopes):
        self.scopes = scopes
        self.http = HTTPClient()
        self.listeners = []

    async def start(self, *, secret: str, id: str):
        await self.login(secret=secret, id=id)
        await self.connect()

    def run(self, *, secret: str, id: str):
        asyncio.run(self.start(secret=secret, id=id))

    async def login(self, *, secret: str, id: str, open_browser: bool=True):
        await self.http.init(secret, id)

        data = await self.http.get_shortcode(list(self.scopes))

        handle = data["handle"]

        code = data["code"]
        url = as_go_link(code)

        if open_browser:
            open_new(url)
            print("If your browser hasn't opened to the link, click here to login:", url)
        else:
            print("Click here to login:", url)

        access_token, refresh_token = await self._wait_for_auth(handle)

        self.oauth = OAuthHandler(self.http, access_token, refresh_token)

        data = await self.http.get_current_user()

        self.current_user = data

    async def connect(self):
        channel_id = self.current_user['channel']['id']
        user_id = self.current_user['channel']['userId']

        ws = WebSocketClient.start(self, channel_id=channel_id, user_id=user_id)
        self.ws = await asyncio.wait_for(ws, timeout=50.0)
        while True:
            await self.ws.handle_message()

    async def send(self, content: str):
        await self.ws.send_message(content)

    async def _wait_for_auth(self, handle: str):
        while True:
            response = await self.http.verify_shortcode(handle)

            try:
                auth = response["code"]
            except TypeError:
                await asyncio.sleep(2)
            else:
                break

        tokens = await self.http.get_tokens(auth)

        return tokens["access_token"], tokens["refresh_token"]

    async def dispatch(self, event_name, *args, **kwargs):
        for listener in self.listeners:
            if listener.name == event_name:
                await listener.execute(*args, **kwargs)

    def event(self, name: str=None):
        def wrapper(coro):
            listener_name = ''

            if name:
                listener_name = name
            else:
                coro_name = coro.__name__
                if coro_name.startswith('on_'):
                    listener_name = coro_name[3:]

            ret = Listener(name=listener_name, callback=coro)
            self.listeners.append(ret)
            return ret
        return wrapper
