from dataclasses import dataclass


@dataclass
class Location:
    latitude: str | None
    longitude: str | None

    def get_coordinates(self) -> tuple:
        return (self.latitude, self.longitude)
    