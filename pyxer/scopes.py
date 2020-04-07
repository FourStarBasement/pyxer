__all__ = [
    'Scopes'
]


class Scope:
    def __init__(self, func):
        self.value = func(None)

    def __get__(self, instance, owner):
        return self.value in self.instance._scopes
    
    def __set__(self, instance, value):
        instance._scopes.append(self.value)


class Scopes:
    def __init__(self):
        self._scopes = []

    @classmethod
    def from_list(self, scopes):
        for scope in scopes:
            scope_attr = scope[scope.index(':') + 1:].replace(':', '_')
            scope_func = setattr(self, scope_attr, True)

    def __iter__(self):
        for s in self._scopes:
            yield s

    @Scope
    def bypass_catbot(self):
        return "chat:bypass_catbot"

    @Scope
    def connect(self):
        return "chat:connect"
    
    @Scope
    def chat(self):
        return "chat:chat"
