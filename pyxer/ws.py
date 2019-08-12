import websockets
from .packet import Packet


class MixerConnection:
    def __init__(self, uri: str):
        self.uri = uri
        self.connection = None

    async def connect(self, channel_id: int, user_id: int, auth_key: str):
        self.connection = await websockets.connect(self.uri)

        await self.login(channel_id, user_id, auth_key)

        async for message in self.connection:
            message = Packet.received(message)
            await self.handle(message["reply"], message)

    async def login(self, *args):
        packet = Packet(type="method", method="auth", arguments=list(args), id=0)

        await self.connection.send(packet.dumped)

    async def handle(self, name, message):
        ...
