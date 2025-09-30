import uuid


class PostTag:
    id_: uuid.UUID
    name: str

    def __init__(self, id_: uuid.UUID, name: str) -> None:
        self.id_ = id_
        self.name = name
