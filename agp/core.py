from dataclasses import asdict
from pathlib import Path
from typing import Union

import pandas
from oidafuel.core import GasPrice, get_gas_stations_by_region, GasStationInfo
from oidafuel.datatypes import FuelType, GasStation
from oidafuel.econtrol import get_regions
from pandas import DataFrame

DATA_PATH = Path("data")
GAS_STATIONS_FILENAME = "gas_stations.csv"
REGIONS_FILENAME = "regions.csv"
CITIES_FILENAME = "cities.csv"
POSTAL_CODES_FILENAME = "postal_codes.csv"

fuel_type_names = {
    FuelType.SUPER_95: "Super 95",
    FuelType.DIESEL: "Diesel",
    FuelType.CNG_ERDGAS: "CNG-Erdgas",
}

GAS_STATION_DTYPES = {
    "station_id": "int64",
    "name": "str",
    "address": "str",
    "postal_code": "str",
    "city": "str",
    "latitude": "float64",
    "longitude": "float64",
}


def get_gas_stations_austria(fuel_type: FuelType) -> list[GasStation]:
    regions = get_regions()
    gas_stations: list[GasStation] = []

    for region in regions:
        print(
            f"Checking {region.name} ({region.region_code}) "
            f"for {fuel_type_names[fuel_type]} prices...",
        )

        for sub_region in region.sub_regions:
            print(
                f"\t{sub_region.name} "
                f"({sub_region.region_code}) "
                f"{fuel_type_names[fuel_type]}...",
                end="",
            )
            new_stations = get_gas_stations_by_region(sub_region.region_code, fuel_type)
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


def update_dataframes(
    original_df: DataFrame, new_df: DataFrame, sort_column
) -> DataFrame:
    columns1 = list(original_df)
    columns2 = list(new_df)

    assert columns1 == columns2
    assert (original_df.dtypes == new_df.dtypes).all()

    df1 = original_df.sort_values(sort_column)
    df2 = new_df.sort_values(sort_column)

    assert len(df1) == len(original_df)
    assert len(df2) == len(new_df)

    unique_df1_ids = df1[sort_column].unique()
    unique_df2_ids = df2[sort_column].unique()

    try:
        assert len(unique_df1_ids) == len(df1)
        assert len(unique_df2_ids) == len(df2)
    except AssertionError as e:
        duplicates1 = df1[df1.station_id.duplicated()]
        duplicates2 = df2[df2.station_id.duplicated()]
        print("Duplicates 1:")
        print(duplicates1)
        print("Duplicates 2:")
        print(duplicates2)
        raise e

    df = pandas.concat([df1, df2])
    df.sort_values(sort_column, inplace=True)
    df.drop_duplicates(sort_column, inplace=True)

    assert len(df) >= len(df1)
    assert len(df) >= len(df2)
    return df


def read_gas_stations_file(
    file_name: Union[str, Path] = "gas_stations.csv",
    data_path: Path = DATA_PATH,
):
    file_path = data_path / file_name

    if file_path.exists():
        return pandas.read_csv(file_path, dtype=GAS_STATION_DTYPES)
    else:
        data = {
            key: pandas.Series(dtype=value) for key, value in GAS_STATION_DTYPES.items()
        }
        return DataFrame(data)


def update_gas_stations_file(
    gas_stations: list[GasStation],
    file_name: Union[str, Path] = GAS_STATIONS_FILENAME,
    data_path: Path = DATA_PATH,
):
    data_path.mkdir(parents=True, exist_ok=True)
    file_path = data_path / file_name

    infos = [GasStationInfo.from_gas_station(station) for station in gas_stations]
    # Drop duplicates, that can happen when two different regions return
    # the same gas station for different times (+-1 Minute) or different fuel types
    infos = list(dict.fromkeys(infos))

    new_dataframe = pandas.DataFrame(infos)
    old_dataframe = read_gas_stations_file(file_name, data_path)

    df = update_dataframes(old_dataframe, new_dataframe, "station_id")
    df.to_csv(file_path, index=False)


def save_regions(
    data_path: Path = DATA_PATH,
):
    regions = get_regions(include_cities=True)
    region_list = []
    city_list = []
    postal_code_list = []

    for region in regions:
        region_dict = asdict(region)
        region_dict.pop("postal_codes")
        region_dict.pop("cities")
        region_dict.pop("sub_regions")
        region_list.append(region_dict)

        for subregion in region.sub_regions:
            subregion_dict = asdict(subregion)
            subregion_dict.pop("postal_codes")
            subregion_dict.pop("cities")
            subregion_dict.pop("sub_regions")
            region_list.append(subregion_dict)

            # Zipping postal codes and city names ist not applicable,
            # because len(postal_codes) != len(city_names) and is ambiguous
            # Example: Oberösterreich has 407 cities and 410 postal codes

            for city_name in subregion.cities:
                city_dict = {
                    "name": city_name,
                    "region_code": subregion.region_code,
                    "state_region_code": region.region_code,
                }
                city_list.append(city_dict)

            for postal_code in subregion.postal_codes:
                postal_code_dict = {
                    "postal_code": postal_code,
                    "region_code": subregion.region_code,
                    "state_region_code": region.region_code,
                }
                postal_code_list.append(postal_code_dict)

    regions_df = pandas.DataFrame(region_list)
    city_df = pandas.DataFrame(city_list)
    postal_code_df = pandas.DataFrame(postal_code_list)

    data_path.mkdir(parents=True, exist_ok=True)
    regions_df.to_csv(data_path / REGIONS_FILENAME, index=False)
    city_df.to_csv(data_path / CITIES_FILENAME, index=False)
    postal_code_df.to_csv(data_path / POSTAL_CODES_FILENAME, index=False)
