from oidafuel.datatypes import FuelType

from agp import __version__
from agp.core import (
    get_gas_prices_vienna,
    save_gas_prices_to_file,
    get_gas_prices_austria,
)


def main():
    print(f"Austrian Gas Prices v{__version__}")

    fuel_types = (FuelType.SUPER_95, FuelType.DIESEL, FuelType.CNG_ERDGAS)

    for fuel_type in fuel_types:
        prices = get_gas_prices_vienna(fuel_type)
        file_name = f"vienna_{fuel_type}.csv"
        save_gas_prices_to_file(prices, file_name)

    # for fuel_type in fuel_types:
    #     prices = get_gas_prices_austria(fuel_type)
    #     file_name = f"austria_{fuel_type}.csv"
    #     save_gas_prices_to_file(prices, file_name)


if __name__ == "__main__":
    main()
