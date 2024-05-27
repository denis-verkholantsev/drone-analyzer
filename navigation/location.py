from dataclasses import dataclass


@dataclass
class Location:
    latitude: float | None
    longitude: float | None

    def get_coordinates(self) -> tuple:
        return (self.latitude, self.longitude)
    