import asyncio
import aiohttp

from route import Route
from mappings.channel import Channel, ExpandedChannel


class HTTPClient:
    def __init__(self, connector=None, *, loop=None):
        self.session = None
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.connector = connector

    async def init(self):
        self.session = aiohttp.ClientSession(connector=self.connector, loop=self.loop)

    async def request(self, route, clazz=None, **kwargs):
        method = route.method
        url = route.url

        async with self.session.request(method, url, **kwargs) as r:
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
                request(route, kwargs)

                return

            if r.status == 403:
                raise Exception('Forbidden.')
            elif r.status == 404:
                raise Exception('Not Found.')


    def get_channel_id(self, username: str):
        '''
        Gets a single user's channel id

        Args:
            username (str): The username whos channel you want to get

        Returns:
            json: The id of the requested user
        '''
        return self.request(Route('GET', '/channels/{username}?fields=id', username=username))

    def get_chat_info(self, channel_id: int):
        '''
        Gets the info of the supplied channel

        Args:
            channel_id (str): The channel whos information you want to get

        Returns:
            json: The channels chatroom settings if authenticated
        '''
        return self.request(Route('GET', '/chats/{channel_id}', channel_id=channel_id))

    def get_channel(self, channel_identifier: str):
        '''
        '''
        return self.request(Route('GET', '/channels/{channel_ident}', channel_ident=channel_identifier), clazz=ExpandedChannel)

    def get_ingests(self):
        return self.request(Route('GET', '/ingests'))
