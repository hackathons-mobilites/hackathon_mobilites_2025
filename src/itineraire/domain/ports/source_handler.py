from abc import ABC, abstractmethod
from shapely.geometry import Point


class SourceHandler(ABC):
    @abstractmethod
    def get_itinerary_transport(self, departure_coordinates: Point, arrival_coordinates: Point) -> dict:
        pass

    @abstractmethod
    def get_itinerary_marche(self, departure_coordinates: Point, arrival_coordinates: Point) -> dict:
        pass

    @abstractmethod
    def get_address_coordinates(self, address_name: str) -> Point:
        pass

    @abstractmethod
    def get_itinerary_velo(
        self,
        departure_coordinates: Point,
        arrival_coordinates: Point,
        profile: str = "Default"
    ) -> list[dict]:
        pass
