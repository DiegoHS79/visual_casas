import os
from datetime import datetime

import pandas as pd

os.system("clear")

path = "../scraping/data_temporal"

files = os.listdir(path)
for file in files:
    df = pd.read_csv(os.path.join(path, file), sep="\t")

    # rest of the columns to numeric data types
    df["Precio m2"] = df["Precio m2"].apply(lambda x: pd.to_numeric(x, errors="coerce"))
    df["Variación mensual"] = df["Variación mensual"].apply(
        lambda x: pd.to_numeric(x, errors="coerce")
    )
    df["Variación trimestral"] = df["Variación trimestral"].apply(
        lambda x: pd.to_numeric(x, errors="coerce")
    )
    df["Variación anual"] = df["Variación anual"].apply(
        lambda x: pd.to_numeric(x, errors="coerce")
    )

    df.to_csv(os.path.join("data", file), index=False, sep="\t")

# the proper way of loading the data frame for having the column "Mes" as datetime format.
# df = pd.read_csv(
#     "data/benalua_la_florida_babel_san_gabriel.csv",
#     sep="\t",
#     parse_dates=["Mes"],
# )
