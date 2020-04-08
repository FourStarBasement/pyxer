from .base import Object, Timestamped
from .channel import Channel


# message authors
class Author(Object):
    def __init__(self, *, client, data):
        super().__init__(client=client)
        self._parse_data(data)

    def _parse_data(self, data):
        self.id = data['user_id']
        self.name = data['user_name']
        self.roles = data['user_roles']
        self.level = data['user_level']
        self.avatar = data['user_avatar']
        self.ascension_level = data['user_ascension_level']


class PartialUser(Object):
    def __init__(self, *, client, data):
        super().__init__(client=client)
        self._parse_data(data)

    def _parse_data(self, data):
        self.id = data['id']
        self.name = data['username']
        self.roles = data['roles']


class User(Timestamped):
    def __init__(self, *, client, data):
        super().__init__(client=client, data=data)
        self._parse_data(data)

    def _parse_data(self, data):
        self.id = data['id']
        self.name = data['username']
        self.channel = Channel(client=self.client, data=data['channel'])
        self.experience = data['experience']
        self.level = data['level']
        self.sparkes = data['sparks']
        self.bio = data['bio']
