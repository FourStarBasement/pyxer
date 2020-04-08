from datetime import datetime


class Object:
    def __init__(self, *, client):
        self.client = client


class Timestamped(Object):
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime

    def __init__(self, *, client, data):
        super().__init__(client=client)

        created_at = data.pop('createdAt', None)
        if created_at:
            self.created_at = datetime.fromisoformat(created_at[:-1])  
            # datetime does not support ISO 8601,
            # but all datetimes should be received as UTC, 
            # so removing "Z" (for UTC) is enough for it to 
            # be parsed properly.
        
        updated_at = data.pop('updatedAt', None)
        if updated_at:
            self.updated_at = datetime.fromisoformat(updated_at[:-1])
        
        deleted_at = data.pop('deletedAt', None)
        if deleted_at:
            self.deleted_at = datetime.fromisoformat(deleted_at[:-1])


class Resource:
    id: int
    type: str
    relid: int
    url: str
    store: str
    remotePath: str
    meta: str = None
