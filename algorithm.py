from datetime import datetime, timedelta
from typing import List, Optional, Tuple
from flight import Flight
from graph import FlightGraph, FlightGraphNodeType
from routes import PartialRoute, Route


class RouteFindingAlgorithm:
    def __init__(self, flights: List[Flight], num_bags: Optional[int] = 0):
        self.flights = flights
        self.num_bags = num_bags
        self.graph = FlightGraph(flights=flights, num_bags=num_bags)

    def find_routes_for_trip(self, origin: str, destination: str, is_round_trip: bool):
        routes = self.find_routes_between(origin, destination)
        # if is_round_trip:
        #     routes_back = self.find_routes_between(destination, origin, num_bags)
        return routes

    def find_routes_between(self, origin: str, destination: str) \
            -> List[Route]:
        solutions = []
        # all possible origin nodes
        q: List[PartialRoute] = [
            PartialRoute([node], 0, timedelta()) for node in self.graph.nodes
            if node.type == FlightGraphNodeType.ORIGIN and node.airport == origin
        ]

        while len(q) > 0:
            current_route = q.pop(0)
            node = current_route.current_node()
            if node.airport == destination:
                if node.type == FlightGraphNodeType.ORIGIN:
                    # todo delete
                    raise Exception("Should not come to destination as origin "
                                    "before we come to destination as destination")
                route = Route(current_route.nodes, origin, destination, self.num_bags,
                              current_route.total_price, current_route.travel_time)
                solutions.append(route)
                continue
            for edge in node.get_neighbors():
                if current_route.contains_airport(edge.to.airport) \
                        or edge.to.flight.bags_allowed < self.num_bags:
                    # No repeating airports in the same trip
                    # and no flights with less bags allowed than necessary
                    print("busted")
                    continue

                new_route = PartialRoute(
                    current_route.nodes + [edge.to],
                    current_route.total_price + edge.price,
                    current_route.travel_time + edge.duration)
                q.append(new_route)

        return solutions
