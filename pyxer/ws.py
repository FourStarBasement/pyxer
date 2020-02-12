import json

import websockets

from .utils import get, as_snake_case


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


class WebSocketClient(websockets.client.WebSocketClientProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.method_calls = []

    @classmethod
    async def start(cls, client, *, channel_id: int, user_id: int):
        data = await client.http.get_connection_info(channel_id)

        uri = data['endpoints'][0]
        auth_key = data['authkey']
        ws = await websockets.connect(uri, extra_headers={'Client-ID': client.http.config.client_id}, klass=cls)

        ws.client = client
        ws.channel_id = channel_id
        ws.user_id = user_id
        ws.uri = uri
        ws.auth_key = auth_key

        return ws

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

    async def handle_message(self):
        try:
            msg = await self.recv()
        except websockets.exceptions.ConnectionClosed as exc:
            print(e)
        else:
            data = Packet.received(msg)
            if data.type == 'event':
                await self.handle(data.event, data)
            elif data.type == 'reply':
                await self.reply(data)

    async def send(self, packet: Packet):
        if packet.type == 'method':
            # Auto ID
            self.method_calls.append(packet)
            packet.set_id(self.method_calls.index(packet))

        await super().send(packet.dumped)

    async def login(self, *args):
        packet = Packet(type="method", method="auth", arguments=list(args))

        await self.send(packet)

    async def send_message(self, content: str):
        packet = Packet(type="method", method="msg", arguments=[content])

        await self.send(packet)

    async def handle(self, name: str, message: Packet):
        name = as_snake_case(name)
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
                print('Could not find original method for reply ID:', id, 'Method:', method.method)
            else:
                await func(method, message)
    
    async def dispatch(self, event_name: str):
        print(event_name)

    async def handle_welcome_event(self, message: Packet):
        await self.login(self.channel_id, self.user_id, self.auth_key)

        await self.dispatch('login')
    
    async def handle_user_join(self, message: Packet):
        print(message.data)

        await self.dispatch('user_join')

    async def handle_chat_message(self, message: Packet):
        print(message.data)

        # TODO: deserialize
        # data: Dict[
        #   channel: int
        #   id: str
        #   name: str
        #   user_id: int
        #   user_roles: List[str]
        #   user_level: int
        #   user_avatar: str
        #   message: List[Dict[
        #       type: str
        #       data: str
        #       text: str
        #   ]]
        #   meta: Dict[]
        # ]

        await self.dispatch('message')

    async def reply_auth(self, sent: Packet, reply: Packet):
        print(reply.data)

        await self.dispatch('login_success')

    async def reply_msg(self, sent: Packet, reply: Packet):
        print(sent.dumped, reply.dumped)
