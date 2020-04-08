from pyxer.client import MixerClient
from pyxer.scopes import Scopes

s = Scopes()

s.bypass_catbot = True
s.connect = True
s.chat = True

mc = MixerClient(scopes=s)

@mc.event("ready")
async def client_ready():
    print('--------------------------')
    print('Logged In As:')
    print('username:', mc.me.name)
    print('id:', mc.me.id)
    print('channel id:', mc.me.channel.id)
    print('---------------------------')

@mc.event("user_join")
async def user_join(user):
    print('User Joined:')
    print('user name:', user.name)
    print('user id:', user.id)
    print('---------------------------')

@mc.event("user_left")
async def user_left(user):
    print('User Left:')
    print('user name:', user.name)
    print('user id:', user.id)
    print('---------------------------')

@mc.event("message")
async def message_handler(message: message.ChatMessage):
    print('New Message:')
    print('channel id:', message.channel.id)
    print('content:', message.content)
    print('author id:', message.author.id)
    print('---------------------------')

mc.run(secret='', id='')
