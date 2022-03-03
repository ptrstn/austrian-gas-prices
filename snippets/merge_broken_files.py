import pandas


def merge_dataframes(df1, df2):
    columns1 = list(df1)
    columns2 = list(df2)

    if columns1 != columns2:
        df1 = df1.reindex(columns=columns2)

    df = pandas.concat([df1, df2])
    return df


def merge_csv_files(file1, file2, out_file_name):
    df1 = pandas.read_csv(file1)
    df2 = pandas.read_csv(file2)

    df = merge_dataframes(df1, df2)
    df.to_csv(out_file_name, index=False)


merge_csv_files(
    "data/austria_DIE.csv", "data/austria_DIE2.csv", "data/austria_DIE3.csv"
)
merge_csv_files(
    "data/austria_SUP.csv", "data/austria_SUP2.csv", "data/austria_SUP3.csv"
)
merge_csv_files(
    "data/austria_GAS.csv", "data/austria_GAS2.csv", "data/austria_GAS3.csv"
)
merge_csv_files("data/vienna_DIE.csv", "data/vienna_DIE2.csv", "data/vienna_DIE3.csv")
merge_csv_files("data/vienna_SUP.csv", "data/vienna_SUP2.csv", "data/vienna_SUP3.csv")
merge_csv_files("data/vienna_GAS.csv", "data/vienna_GAS2.csv", "data/vienna_GAS3.csv")
