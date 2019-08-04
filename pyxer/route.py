from urllib.parse import quote


class Route:
    BASE_ROUTE = 'https://mixer.com/api/v1'

    def __init__(self, method, path, **kwargs):
        self.method = method
        self.route = path

        self.url = self.BASE_ROUTE + self.route
        if kwargs:
            format_dict = {param: quote(value) for param, value in kwargs.items()}
            self.url = self.url.format_map(format_dict)
