from .http import HTTPClient
from .ws import MixerConnection


class MixerClient:
    def __init__(self, **kwargs):
        self.http = HTTPClient()

        self._channel_id = kwargs.get('channel_id')
        self._username = kwargs.get('username')

        if self._username and self._channel_id:
            raise Exception('you can only use channel_id, **or** username, not both.')

        self.wss_addr = None
        self.auth_key = ''

        self._connection = None

    async def login(self):
        await self.http.init()

        if self._username:
            self._channel_id = await self.fetch_channel_id(self._username)

        chat_data = await self.http.get_chat_info(self._channel_id)

        self.wss_addr = chat_data['endpoints']
        self.auth_key = chat_data['authkey']

    async def connect(self):
        # TODO: Start websocket connection
        return

    async def fetch_channel_id(self, username: str):
        return await self.http.get_channel_id(self._username)['id']
