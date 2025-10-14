import uuid


class User:
    id_: uuid.UUID
    username: str

    def __init__(self, id_: uuid.UUID, username: str):
        self.username = username
        self.id_ = id_
