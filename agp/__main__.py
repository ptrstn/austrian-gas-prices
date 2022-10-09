import argparse
import datetime

from oidafuel.core import gas_stations_to_gas_prices
from oidafuel.datatypes import FuelType

from agp import __version__
from agp.core import (
    save_gas_prices_to_file,
    get_gas_stations_vienna,
    get_gas_stations_austria,
    update_gas_stations_file,
)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Python client retrieve austrian gas prices"
    )

    parser.add_argument(
        "--version", action="version", version="%(prog)s {}".format(__version__)
    )

    parser.add_argument(
        "--vienna",
        help="Retrieve gas prices for all regions of vienna",
        action="store_true",
    )
    parser.add_argument(
        "--austria",
        help="Retrieve gas prices for all regions of austria",
        action="store_true",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    print(f"Austrian Gas Prices (agp), v{__version__}\n")

    fuel_types = (FuelType.SUPER_95, FuelType.DIESEL, FuelType.CNG_ERDGAS)

    now = datetime.datetime.now()

    if args.austria:
        print("== Austria ==")
        for fuel_type in fuel_types:
            stations = get_gas_stations_austria(fuel_type)
            update_gas_stations_file(stations)
            prices = gas_stations_to_gas_prices(stations)
            assert len(prices) == len(set(prices))

            file_name = f"austria_{fuel_type}_{now.year}_{now.month}.csv"
            save_gas_prices_to_file(prices, file_name)


if __name__ == "__main__":
    main()
