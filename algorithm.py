from datetime import datetime, timedelta
from typing import List, Optional, Tuple
from flight import Flight
from graph import FlightGraph, FlightGraphNodeType, FlightGraphNode
from routes import PartialRoute, Route


class RouteFindingAlgorithm:
    def __init__(self, flights: List[Flight], num_bags: int):
        self.flights = flights
        self.num_bags = num_bags
        self.graph = FlightGraph(flights=flights, num_bags=num_bags)

    def find_routes_for_trip(self, origin: str, destination: str, is_round_trip: bool):
        destination_routes = self.find_routes_between(origin, destination)

        if is_round_trip:
            routes = []
            # find the return flights individually for each of the found routes
            for dest_route in destination_routes:
                # Layover rule doesn't apply, however it is still assumed here that at least 1 hour should be spent
                # in the destination location before going back
                time_lower_bound = dest_route.current_node().time + timedelta(hours=1)
                return_routes = self.find_routes_between(destination, origin, time_lower_bound)
                routes += [
                    Route.concatenate(dest_route, return_route) for return_route in return_routes
                ]

        else:
            routes = destination_routes

        return routes

    def find_routes_between(self, origin: str, destination: str, time_lower_bound: Optional[datetime] = None)\
            -> List[Route]:
        solutions = []

        def is_valid_start_node(node: FlightGraphNode) -> bool:
            # Each successive node will necessarily have time > time of the origin node thus we only
            # need to check the time lower bound here
            return node.type == FlightGraphNodeType.ORIGIN and node.airport == origin \
                   and (time_lower_bound is None or node.time >= time_lower_bound)

        # all possible origin nodes
        q: List[PartialRoute] = [
            PartialRoute([node], 0, timedelta()) for node in self.graph.nodes
            if is_valid_start_node(node)
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
                if current_route.contains_origin_airport(edge.to.airport) \
                        or edge.to.flight.bags_allowed < self.num_bags:
                    # No repeating airports in the same trip
                    # and no flights with less bags allowed than necessary
                    continue

                new_route = PartialRoute(
                    current_route.nodes + [edge.to],
                    current_route.total_price + edge.price,
                    current_route.travel_time + edge.duration)
                q.append(new_route)

        return solutions
