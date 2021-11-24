import argparse
import json
from datetime import datetime
from typing import Optional, Final, List

from algorithm import RouteFindingAlgorithm
from flight import Flight


class Solution:
    def run(self):
        parser = argparse.ArgumentParser(description='Optional app description')
        self.add_arguments(parser)
        args = parser.parse_args()
        result = self.handle(**args.__dict__)
        print(json.dumps(result, indent=4))

    @staticmethod
    def add_arguments(parser):
        parser.add_argument('data_path', type=str, help='Path to the data file')
        parser.add_argument('origin', type=str, help='Source airport code')
        parser.add_argument('--bags', type=int, help='Number of bags', default=0)
        parser.add_argument('destination', type=str, help='Destination airport code')
        parser.add_argument('--return', action='store_true', dest='is_round_trip',
                            help='A boolean indicating whether the trip is round-trip')

    def handle(self, data_path: str, origin: str, destination: str, bags: int, is_round_trip: bool) -> List[dict]:
        flights = self.read_dataset(path=data_path)

        algo = RouteFindingAlgorithm(flights, num_bags=bags)
        routes = algo.find_routes_for_trip(origin, destination, is_round_trip)

        # Output is sorted by the final price of the trip
        routes = sorted(routes, key=lambda x: x.total_price)
        return [r.as_dict() for r in routes]

    @staticmethod
    def read_dataset(path: str) -> List[Flight]:
        with open(path, 'r') as f:
            headers, *rows = map(lambda x: x.strip().split(','), f.readlines())

        flights = [
            Flight(flight_no=row[0],
                   origin=row[1],
                   destination=row[2],
                   departure=row[3],
                   arrival=row[4],
                   base_price=float(row[5]),
                   bag_price=float(row[6]),
                   bags_allowed=int(row[7]))
            for row in rows
        ]
        return flights


if __name__ == "__main__":
    # python -m solution example/example0.csv RFZ WIW --bags=1 --return
    Solution().run()
