from pyxer.client import MixerClient
from pyxer.scopes import Scopes

s = Scopes()

s.bypass_catbot = True
s.connect = True
s.chat = True

mc = MixerClient(scopes=s)

@mc.event("login_success")
async def login_success():
    print('--------------------------')
    print('Logged In As:')
    print('username:', mc.current_user['username'])
    print('id:', mc.current_user['id'])
    print('---------------------------')

@mc.event("user_join")
async def user_join(user):
    print('User Joined:')
    print('user name:', user.data['username'])
    print('user id:', user.data['id'])
    print('---------------------------')

@mc.event("user_left")
async def user_left(user):
    print('User Left:')
    print('user name:', user.data['username'])
    print('user id:', user.data['id'])
    print('---------------------------')

@mc.event("message")
async def message_handler(message):
    print('New Message:')
    print('content:', message.data['message']['message'][0]['text'])
    print('author name:', message.data['user_name'])
    print('author id:', message.data['user_id'])
    print('---------------------------')

mc.run(secret='', id='')
