from pathlib import Path

import pandas
from oidafuel.datatypes import FuelType

from agp.core import (
    get_gas_stations_vienna,
    get_gas_stations_austria,
    update_gas_stations_file,
    save_regions,
    REGIONS_FILENAME,
    CITIES_FILENAME,
    POSTAL_CODES_FILENAME,
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


def test_save_regions():
    data_path = Path("test_data")
    regions_path = data_path / REGIONS_FILENAME
    cities_path = data_path / CITIES_FILENAME
    postal_codes_path = data_path / POSTAL_CODES_FILENAME

    assert not regions_path.exists()
    assert not cities_path.exists()
    assert not postal_codes_path.exists()
    save_regions(data_path=data_path)
    assert regions_path.exists()
    assert cities_path.exists()
    assert postal_codes_path.exists()

    regions = pandas.read_csv(regions_path)
    postal_codes = pandas.read_csv(postal_codes_path)
    cities = pandas.read_csv(cities_path)

    assert len(regions) == 126
    assert "region_code" in regions
    assert "postal_code" in postal_codes
    assert "name" in cities

    regions_path.unlink()
    postal_codes_path.unlink()
    cities_path.unlink()
