from datetime import datetime
from typing import Final


class Flight:
    DATE_SERIALIZATION_FORMAT: Final = '%Y-%m-%dT%H:%M:%S'

    def __init__(self, flight_no: str, origin: str, destination: str, departure: str, arrival: str,
                 base_price: float, bag_price: float, bags_allowed: int):
        self.flight_no = flight_no
        self.origin = origin
        self.destination = destination
        self.departure = self.parse_datetime(departure)
        self.arrival = self.parse_datetime(arrival)
        self.base_price = base_price
        self.bag_price = bag_price
        self.bags_allowed = bags_allowed

    def __str__(self):
        return f"Flight {self.flight_no} from {self.origin} to {self.destination} on {self.departure} " \
               f"with {self.bags_allowed} allowed bags"

    def __repr__(self):
        return self.__str__()

    def get_price(self, bags_count: int) -> float:
        return self.base_price + self.bag_price * bags_count

    @classmethod
    def parse_datetime(cls, dt_str: str) -> datetime:
        return datetime.strptime(dt_str, cls.DATE_SERIALIZATION_FORMAT)

    @classmethod
    def format_datetime(cls, dt: datetime) -> str:
        return datetime.strftime(dt, cls.DATE_SERIALIZATION_FORMAT)

    def as_dict(self):
        return {
            "flight_no": self.flight_no,
            "origin": self.origin,
            "destination": self.destination,
            "departure": self.format_datetime(self.departure),
            "arrival": self.format_datetime(self.arrival),
            "base_price": self.base_price,
            "bag_price": self.bag_price,
            "bags_allowed": self.bags_allowed,
        }
