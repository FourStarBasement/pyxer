import asyncio
import aiohttp

from .route import Route


class HTTPClient:
    def __init__(self, connector=None, *, loop=None):
        self.session = None
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.connector = connector

    async def init(self):
        self.session = aiohttp.ClientSession(connector=self.connector, loop=self.loop)

    async def request(self, route, **kwargs):
        method = route.method
        url = route.url

        async with self.session.request(method, url, **kwargs) as r:
            data = await r.json() if r.headers['content-type'] == 'application/json' else r.text(encoding='utf-8')

            if 300 > r.status >= 200:
                return data

            if r.status == 429:
                retry_after = data['retry_after'] / 1000.0

                raise Exception('Rate limited! Retry after {} seconds.'.format(retry_after))

            if r.status == 403:
                raise Exception('Forbidden.')
            elif r.status == 404:
                raise Exception('Not Found.')
            else:
                raise Exception(data)

    def get_channel_id(self, username: str):
        return self.request(Route('GET', '/channels/{username}?fields=id', username=username))

    def get_chat_info(self, channel_id: int):
        return self.request(Route('GET', '/chats/{channel_id}', channel_id=channel_id))
