import json


class Packet:
    def __init__(self, **kwargs):
        self._packet = dict(kwargs)

        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def dumped(self):
        return json.dumps(self._packet)

    @classmethod
    def received(cls, msg):
        return cls(**json.loads(msg))
