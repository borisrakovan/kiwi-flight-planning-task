import argparse
import json
from datetime import datetime
from typing import Optional, Final, List

from algorithm import RouteFindingAlgorithm
from flight import Flight


class TaskRunner:
    DATA_HEADERS: Final = ["flight_no", "origin", "destination", "departure", "arrival", "base_price", "bag_price",
                           "bags_allowed"]

    def run(self):
        print("Hello world")
        parser = argparse.ArgumentParser(description='Optional app description')

        self.add_arguments(parser)
        args = parser.parse_args()

        # self.handle(args.data_path, args.origin, args.destination, args.bags, args.is_return)
        result = self.handle(**args.__dict__)
        print(
            json.dumps(result, indent=4)
        )

    @staticmethod
    def add_arguments(parser):
        parser.add_argument('data_path', type=str, help='Path to the data file')
        parser.add_argument('origin', type=str, help='Source airport code')
        parser.add_argument('--bags', type=int, help='Number of bags')
        parser.add_argument('destination', type=str, help='Destination airport code')
        parser.add_argument('--return', action='store_false', dest='is_round_trip',
                            help='A boolean indicating whether the trip is round-trip')

    def handle(self, data_path: str, origin: str, destination: str,
               bags: Optional[int], is_round_trip: Optional[bool] = False):
        print(data_path)
        print(f"{origin} -> {destination} {bags} {is_round_trip}")

        flights = self.read_dataset(path=data_path)

        algo = RouteFindingAlgorithm(flights, num_bags=bags)

        routes = algo.find_routes_for_trip(origin, destination, is_round_trip)
        print(f"FOUND {len(routes)} solutions:")
        for r in routes:
            print(r)

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
    TaskRunner().run()
