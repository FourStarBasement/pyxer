from typing import Text, Coroutine


class Listener:
    name: Text
    callback: Coroutine

    def __init__(self, *, name, callback):
        self.name = name
        self.callback = callback

    def error(self, coro):
        self.on_error = coro
    
    async def raise_error(self, exc):
        try:
            handler = self.on_error
        except AttributeError:
            raise exc
        else:
            await handler(exc)

    async def execute(self, *args, **kwargs):
        try:
            await self.callback(*args, **kwargs)
        except Exception as exc:
            await self.raise_error(exc)
