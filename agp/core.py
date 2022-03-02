from pathlib import Path
from typing import Union

import pandas
from oidafuel.core import GasPrice, get_gas_prices_by_region
from oidafuel.datatypes import FuelType
from oidafuel.econtrol import get_regions

DATA_PATH = Path("data")

fuel_type_names = {
    FuelType.SUPER_95: "Super 95",
    FuelType.DIESEL: "Diesel",
    FuelType.CNG_ERDGAS: "CNG-Erdgas",
}


def get_gas_prices_vienna(fuel_type: FuelType) -> list[GasPrice]:
    gas_prices = []
    for region_code in range(900, 923 + 1):
        print(
            f"Checking region {region_code} "
            f"for {fuel_type_names[fuel_type]} prices... ",
            end="",
        )
        new_prices = get_gas_prices_by_region(region_code, fuel_type)
        print(f"({len(new_prices)} found)")
        gas_prices.extend(new_prices)
    return gas_prices


def get_gas_prices_austria(fuel_type: FuelType) -> list[GasPrice]:
    regions = get_regions()
    gas_prices = []
    for region in regions:
        print(
            f"{region.name} ({region.region_code}) "
            f"for {fuel_type_names[fuel_type]} prices...",
            end="",
        )
        new_prices = get_gas_prices_by_region(region.region_code, fuel_type)
        print(f"({len(new_prices)} found)")
        gas_prices.extend(new_prices)

        for sub_region in region.sub_regions:
            print(
                f"\t{sub_region.name} "
                f"({sub_region.region_code}) "
                f"{fuel_type_names[fuel_type]}...",
                end="",
            )
            new_prices = get_gas_prices_by_region(region.region_code, fuel_type)
            print(f"({len(new_prices)} found)")
            gas_prices.extend(new_prices)
    return gas_prices


def save_gas_prices_to_file(gas_prices: list[GasPrice], file_name: Union[str, Path]):
    dataframe = pandas.DataFrame(gas_prices)
    file_path = DATA_PATH / file_name

    kwargs = {"path_or_buf": file_path, "index": False, "mode": "a"}
    if file_path.exists():
        kwargs["header"] = False

    print(f"Saving {len(gas_prices)} gas prices in {file_name}...")
    file_path.parent.mkdir(parents=True, exist_ok=True)

    dataframe.to_csv(**kwargs)
