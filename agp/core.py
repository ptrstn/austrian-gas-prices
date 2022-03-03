from pathlib import Path
from typing import Union

import pandas
from oidafuel.core import GasPrice, get_gas_stations_by_region, GasStationInfo
from oidafuel.datatypes import FuelType, GasStation
from oidafuel.econtrol import get_regions

DATA_PATH = Path("data")

fuel_type_names = {
    FuelType.SUPER_95: "Super 95",
    FuelType.DIESEL: "Diesel",
    FuelType.CNG_ERDGAS: "CNG-Erdgas",
}


def get_gas_stations_austria(fuel_type: FuelType) -> list[GasStation]:
    regions = get_regions()
    gas_stations = []

    for region in regions:
        print(
            f"Checking {region.name} ({region.region_code}) "
            f"for {fuel_type_names[fuel_type]} prices...",
            end="",
        )
        new_stations = get_gas_stations_by_region(region.region_code, fuel_type)
        print(f"({len(new_stations)} found)")
        gas_stations.extend(new_stations)

        for sub_region in region.sub_regions:
            print(
                f"\t{sub_region.name} "
                f"({sub_region.region_code}) "
                f"{fuel_type_names[fuel_type]}...",
                end="",
            )
            new_stations = get_gas_stations_by_region(region.region_code, fuel_type)
            print(f"({len(new_stations)} found)")
            gas_stations.extend(new_stations)

    unique_stations = list(dict.fromkeys(gas_stations))
    return unique_stations


def get_gas_stations_vienna(fuel_type: FuelType) -> list[GasStation]:
    regions = get_regions()
    vienna_region = regions[8]
    assert vienna_region.name == "Wien"
    gas_stations = []

    for region in vienna_region.sub_regions:
        print(
            f"Checking {region.name} ({region.region_code}) "
            f"for {fuel_type_names[fuel_type]} prices...",
            end="",
        )
        new_stations = get_gas_stations_by_region(region.region_code, fuel_type)
        print(f"({len(new_stations)} found)")
        gas_stations.extend(new_stations)

    unique_stations = list(dict.fromkeys(gas_stations))
    return unique_stations


def save_gas_prices_to_file(gas_prices: list[GasPrice], file_name: Union[str, Path]):
    dataframe = pandas.DataFrame(gas_prices)
    file_path = DATA_PATH / file_name

    kwargs = {"path_or_buf": file_path, "index": False, "mode": "a"}
    if file_path.exists():
        kwargs["header"] = False

    print(f"Saving {len(gas_prices)} gas prices in {file_name}...")
    file_path.parent.mkdir(parents=True, exist_ok=True)

    dataframe.to_csv(**kwargs)


def update_gas_stations_file(
    gas_stations: list[GasStation],
    file_name: Union[str, Path] = "gas_stations.csv",
    data_path: Path = DATA_PATH,
):
    data_path.mkdir(parents=True, exist_ok=True)
    file_path = data_path / file_name

    infos = [GasStationInfo.from_gas_station(station) for station in gas_stations]

    new_dataframe = pandas.DataFrame(infos)
    old_dataframe = pandas.read_csv(file_path) if file_path.exists() else new_dataframe
    df = (
        pandas.concat([old_dataframe, new_dataframe])
        .drop_duplicates()
        .sort_values("station_id")
    )

    df.to_csv(file_path, index=False)


def renew_data(path, a):
    df = pandas.read_csv(path)
    info_columns = [
        "identifier",
        "name",
        "address",
        "city",
        "postal_code",
        "latitude",
        "longitude",
    ]
    price_columns = ["identifier", "fuel_type", "label", "price", "timestamp"]

    info_df = df[info_columns].copy()
    info_df.rename(columns={"identifier": "station_id"}, inplace=True)
    info_df.sort_values("station_id", inplace=True)
    info_df.drop_duplicates(inplace=True)
    info_df.to_csv(a, index=False)

    price_df = df[price_columns].copy()
    price_df.rename(columns={"identifier": "station_id"}, inplace=True)
    price_df.drop_duplicates(inplace=True)
    price_df.to_csv(path, index=False)


def renew_info():
    files = [
        "gas_stations_austria_DIE.csv",
        "gas_stations_austria_GAS.csv",
        "gas_stations_austria_SUP.csv",
        "gas_stations_vienna_DIE.csv",
        "gas_stations_vienna_GAS.csv",
        "gas_stations_vienna_SUP.csv",
    ]
    path = "data.bak"
    dfs = [pandas.read_csv(f"{path}/{file}") for file in files]
    df = pandas.concat(dfs).drop_duplicates().sort_values("station_id")
    df.to_csv("data.bak/gas_stations.csv", index=False)
