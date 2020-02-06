import json
import websockets

from .utils import get


class Packet:
    def __init__(self, **kwargs):
        self._packet = dict(kwargs)

        for k, v in kwargs.items():
            setattr(self, k, v)

    def set_id(self, id: int):
        self._packet['id'] = id
        self.id = id

    @property
    def dumped(self):
        return json.dumps(self._packet)

    @classmethod
    def received(cls, msg):
        return cls(**json.loads(msg))


class WebSocketClient:
    def __init__(self, uri: str):
        self.uri = uri
        self.connection = None
        self.method_calls = []

    async def connect(self, channel_id: int, user_id: int, client_id: str, auth_key: str):
        self.channel_id = channel_id
        self.user_id = user_id
        self.client_id = client_id
        self.auth_key = auth_key
        self.connection = await websockets.connect(self.uri, extra_headers={'Client-ID': client_id})

        async for message in self.connection:
            message = Packet.received(message)
            if message.type == 'event':
                await self.handle(message.event, message)
            elif message.type == 'reply':
                await self.reply(message)

    async def send(self, packet: Packet):
        if packet.type == 'method':
            # Auto ID
            self.method_calls.append(packet)
            packet.set_id(self.method_calls.index(packet))

        await self.connection.send(packet.dumped)

    async def login(self, *args):
        packet = Packet(type="method", method="auth", arguments=list(args))

        await self.send(packet)

    async def handle(self, name, message):
        func_name = f'handle_{name}'

        try:
            func = getattr(self, func_name)
        except AttributeError:
            print('Could not handle event', name)
        else:
            await func(message)

    async def reply(self, message: Packet):
        id = message.id
        method = get(self.method_calls, 'id', id)

        if method:
            func_name = f'reply_{method.method}'

            try:
                func = getattr(self, func_name)
            except AttributeError:
                print('Could not find original method for reply ID:', id)
            else:
                await func(method, message)

    async def handle_WelcomeEvent(self, message: Packet):
        await self.login(self.channel_id, self.user_id, self.auth_key)
    
    async def handle_UserJoin(self, message: Packet):
        print(message.data)

    async def reply_auth(self, sent: Packet, reply: Packet):
        print(reply.data)
