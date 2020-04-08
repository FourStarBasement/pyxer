from functools import reduce

def as_go_link(code: str):
    return "https://mixer.com/go?code={}".format(code)

def get(objects, attr, value):
    for obj in objects:
        if getattr(obj, attr, None) == value:
            return obj
        elif isinstance(obj, dict) and obj.get(attr) == value:
            return obj

def as_snake_case(name: str):
    return reduce(lambda v, e: v + ('_' if e.isupper() else '') + e, name).lower()
