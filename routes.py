from datetime import timedelta
from typing import List

from graph import FlightGraphNodeType, FlightGraphNode


class PartialRoute:
    def __init__(self, nodes: List[FlightGraphNode], total_price: float, travel_time: timedelta):
        self.nodes = nodes
        self.total_price = total_price
        self.travel_time = travel_time

    def __str__(self):
        return " -> ".join([node.airport for node in self.nodes])

    def current_node(self):
        return self.nodes[-1]

    def add_node(self, node: FlightGraphNode):
        self.nodes.append(node)

    def contains_origin_airport(self, airport: str):
        # The same airport cannot appear twice as the origin airport
        return airport in [node.airport for node in self.nodes if node.type == FlightGraphNodeType.ORIGIN]


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

    @classmethod
    def concatenate(cls, route_a: 'Route', route_b: 'Route'):
        if route_a.current_node().airport != route_b.nodes[0].airport:
            raise ValueError("Cannot concatenate routes with non-matching airports")

        return cls(
            # More robust solution would be to concatenate the copies of nodes but since they are not mutated it
            # is not necessary
            nodes=route_a.nodes + route_b.nodes,
            origin=route_a.origin,
            destination=route_b.destination,
            bags_count=route_a.bags_count,
            total_price=route_a.total_price + route_b.total_price,
            travel_time=route_a.travel_time + route_b.travel_time)

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
