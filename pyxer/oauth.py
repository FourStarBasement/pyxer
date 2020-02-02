import asyncio
from datetime import datetime, timedelta

from .http import HTTPClient


class OAuthHandler:
    http: HTTPClient
    access_token: str
    refresh_token: str

    def __init__(self, http: HTTPClient, access_token: str, refresh_token: str):
        self.http = http
        self.access_token = access_token
        self.http.update_token(self.access_token)
        self.refresh_token = refresh_token

        asyncio.create_task(self.refresh_task())

    async def refresh_task(self):
        await asyncio.sleep(21600)
        data = self.http.refresh_tokens(self.refresh_token)
        self.access_token = data["access_token"]
        self.refresh_token = data["refresh_token"]
        self.http.update_token(self.access_token)
        
