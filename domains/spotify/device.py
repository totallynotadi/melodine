from typing import Dict


class Device:
    def __init__(self, data: Dict) -> None:
        self.id: str = data.get('id')
        self.name: str = data.get('name')
        self.type: str = data.get('type')

        self.volume: int = data.get('volume')

        self.is_active: bool = data.get('is_active')
        self.is_private_session: bool = data.get('is_private_session')
        self.is_restricted = data.get('is_restricted')

    def __eq__(self, other):
        return type(self) is type(other) and self.id == other.id

    def __repr__(self):
        return f"<spotify.Device: {(self.name or self.id)!r}>"

    def __str__(self):
        return self.id
