from typing import List, Dict
from .base import Timestamped, Resource
from .channel import Channel
from .user import Author


class MessageContent:
    def __init__(self, message_list):
        self._message_list = message_list
    
    def __str__(self):
        return ''.join(m['text'] for m in self._message_list)

class ChatMessage(Timestamped):
    def __init__(self, *, client, data):
        super().__init__(client=client, data=data)
    
    @classmethod
    async def _received(cls, *, client, data):
        inst = cls(client=client, data=data)
        inst.channel = await client.find_channel(data.pop('channel'))
        inst.id = data.pop('id')
        inst.content = MessageContent(data.pop('message')['message'])
        inst.author = Author(client=client, data=data)

        return inst
