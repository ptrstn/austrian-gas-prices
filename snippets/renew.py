import pandas


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
