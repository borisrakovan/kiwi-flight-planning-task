from datetime import timedelta
from typing import List

from graph import FlightGraphNodeType, FlightGraphNode


class PartialRoute:
    def __init__(self, nodes: List[FlightGraphNode], total_price: float, travel_time: timedelta):
        self.nodes = nodes
        self.total_price = total_price
        self.travel_time = travel_time

    def current_node(self):
        return self.nodes[-1]

    def add_node(self, node: FlightGraphNode):
        self.nodes.append(node)

    def contains_airport(self, airport: str):
        return airport in [node.airport for node in self.nodes]


class Route(PartialRoute):
    def __init__(self, nodes: List[FlightGraphNode], origin: str, destination: str, bags_count: int,
                 total_price: float, travel_time: timedelta):
        super().__init__(nodes, total_price, travel_time)
        self.origin = origin
        self.destination = destination
        self.bags_count = bags_count

        self.validate()
        # take the flight object of every other node
        self.flights = [
            node.flight for i, node in enumerate(self.nodes)
            if i % 2 == 0
        ]
        self.bags_allowed = min(f.bags_allowed for f in self.flights)
        # todo delete
        assert self.bags_allowed >= self.bags_count

    def __str__(self):
        return " -> ".join([node.airport for node in self.nodes])

    # todo delete
    def validate(self):
        expecting_origin = True
        for node in self.nodes:
            if expecting_origin and node.type != FlightGraphNodeType.ORIGIN:
                raise ValueError("Expecting origin node")
            if not expecting_origin and node.type != FlightGraphNodeType.DESTINATION:
                raise ValueError("Expecting destination node")

            expecting_origin = not expecting_origin

    def as_dict(self):
        return {
            "flights": [flight.as_dict() for flight in self.flights],
            "origin": self.origin,
            "destination": self.destination,
            "bags_allowed": self.bags_allowed,
            "bags_count": self.bags_count,
            "total_price": self.total_price,
            "travel_time":  str(self.travel_time),
        }
