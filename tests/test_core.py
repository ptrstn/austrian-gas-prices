from pathlib import Path

from oidafuel.datatypes import FuelType

from agp.core import (
    get_gas_stations_vienna,
    get_gas_stations_austria,
    update_gas_stations_file,
)


def test_get_gas_stations_vienna():
    fuel_type = FuelType.SUPER_95
    stations = get_gas_stations_vienna(fuel_type)
    unique_stations = set(stations)
    assert len(stations) == len(unique_stations)


def test_get_gas_stations_austria():
    fuel_type = FuelType.SUPER_95
    stations = get_gas_stations_austria(fuel_type)
    unique_stations = set(stations)
    assert len(stations) == len(unique_stations)


def test_update_gas_stations_file():
    data_path = Path("test_data")
    fuel_type = FuelType.SUPER_95
    stations = get_gas_stations_vienna(fuel_type)

    update_gas_stations_file(gas_stations=stations, data_path=data_path)
