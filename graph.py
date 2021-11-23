from datetime import timedelta, datetime
from enum import Enum
from typing import Optional, List

from flight import Flight


class FlightGraphNodeType(Enum):
    ORIGIN = 1
    DESTINATION = 2


class FlightGraphEdge:
    def __init__(self, to: 'FlightGraphNode', price: float, duration: timedelta):
        self.to = to
        self.price = price
        self.duration = duration


class FlightGraphNode:
    def __init__(self, flight: Flight, node_type: FlightGraphNodeType, airport: str, time: datetime):
        self.flight = flight
        self.type = node_type
        self.airport = airport
        self.time = time
        self.neighbors: List[FlightGraphEdge] = []

    def add_neighbor(self, node: 'FlightGraphNode', price: float, duration: timedelta):
        self.neighbors.append(FlightGraphEdge(node, price, duration))

    def get_neighbors(self) -> List[FlightGraphEdge]:
        return self.neighbors


class FlightGraph:
    """
        Nodes are departures and arrivals,
        edges are flights or layovers with the price indicating the price of the flight or 0 in case of layover
        and the duration indicating the duration of the flight or the layover

    """
    def __init__(self, flights: List[Flight], num_bags: int):
        self.flights = flights
        self.num_bags = num_bags
        self.nodes: List[FlightGraphNode] = []
        self.create_graph()

    @staticmethod
    def is_valid_layover(node_a: FlightGraphNode, node_b: FlightGraphNode,
                         min_layover_hours: Optional[int] = 1, max_layover_hours: Optional[int] = 6):
        if node_a.airport != node_b.airport:
            return False
        if node_a.type != FlightGraphNodeType.DESTINATION or node_b.type != FlightGraphNodeType.ORIGIN:
            return False
        layover_time = node_b.time - node_a.time
        # In case of a combination of A -> B -> C, the layover time in B should not be less than 1 hour
        # and more than 6 hours
        layover_time_valid = timedelta(hours=min_layover_hours) <= layover_time <= timedelta(hours=max_layover_hours)
        return layover_time_valid

    def create_graph(self):
        for flight in self.flights:
            origin_node = FlightGraphNode(flight=flight, node_type=FlightGraphNodeType.ORIGIN,
                                          airport=flight.origin, time=flight.departure)
            dest_node = FlightGraphNode(flight=flight, node_type=FlightGraphNodeType.DESTINATION,
                                        airport=flight.destination, time=flight.arrival)
            self.nodes.append(origin_node)
            self.nodes.append(dest_node)
            duration = dest_node.time - origin_node.time
            price = flight.base_price + flight.bag_price * self.num_bags
            origin_node.add_neighbor(dest_node, price, duration)

        for node_a in self.nodes:
            for node_b in self.nodes:
                if self.is_valid_layover(node_a, node_b):
                    layover_time = node_b.time - node_a.time
                    node_a.add_neighbor(node_b, 0, layover_time)
