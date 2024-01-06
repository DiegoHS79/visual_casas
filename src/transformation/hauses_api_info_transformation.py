import os
import re
import json

import numpy as np
import pandas as pd

os.system("clear")

path = "../api/data"
file_name = "data_hauses.csv"

distritos = {
    "Benalúa-La Florida-Babel-San Gabriel": "benalua",
    "Campoamor-Carolinas-Altozano": "campoamor",
    "Centro": "centro",
    "Parque Avenidas - Vistahermosa": "vistahermosa",
    "Playa de San Juan-El Cabo": "sanjuan",
    "San Blas-Pau": "sanblas",
}

df = pd.read_csv(os.path.join(path, file_name), sep="\t")

# loop over distritos
for dist, name in list(distritos.items()):
    df_tmp = df[df.district == dist]
    df_tmp.to_csv(os.path.join(path, f"{name}.csv"), index=False, sep="\t")
