def as_go_link(code: str):
    return "https://mixer.com/go?code={}".format(code)

def get(objects, attr, value):
    for obj in objects:
        if getattr(obj, attr, None) == value:
            return obj
