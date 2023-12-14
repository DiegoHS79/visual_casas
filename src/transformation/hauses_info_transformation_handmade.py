import os
import re
import json

import numpy as np
import pandas as pd

os.system("clear")

path = "../scraping/data_hause"

handmade_file = "hause_info_summary_handmade.json"

with open(os.path.join(path, handmade_file), "r") as fi:
    idealista_info = json.load(fi)

columns = [
    "id",
    "url",
    "distrito",
    "barrio",
    "price (\u20ac)",
    "bedrooms",
    "area (m2)",
    "floor",
    "lift",
    "street type",
    "street",
    "street_number",
]

final_df = pd.DataFrame(columns=columns)
for i, hause_id in enumerate(list(idealista_info.keys())):
    # if i != 3:
    #     continue
    # print(json.dumps(idealista_info[hause_id], indent=4))

    hause_data = idealista_info[hause_id]

    df_tmp = pd.DataFrame([[np.nan] * len(columns)], columns=columns)
    df_tmp["id"] = hause_data["id"]
    df_tmp["url"] = hause_data["url"]
    df_tmp["distrito"] = hause_data["distrito"]
    df_tmp["barrio"] = hause_data["barrio"]
    df_tmp["price (\u20ac)"] = int(hause_data["price"].strip("\u20ac").replace(".", ""))
    details = hause_data["details"]
    for detail in details:
        if "hab." in detail:
            df_tmp["bedrooms"] = int(detail.strip("hab. "))
        elif "m\u00b2" in detail:
            df_tmp["area (m2)"] = int(detail.strip("m\u00b2 ").replace(".", ""))
        elif "bajo" in detail.lower():
            df_tmp["floor"] = 0
        elif "\u00aa" in detail:
            df_tmp["floor"] = re.findall(r"\d+", detail)[0]
        if "con ascensor" in detail:
            df_tmp["lift"] = "yes"
        elif "sin ascensor" in detail:
            df_tmp["lift"] = "no"

    title = hause_data["title"].lower().replace("\n", "")
    if "avenida" in title:
        df_tmp["street type"] = "avenida"
        df_tmp["street"] = title.split(",")[0].split("avenida")[-1]
    elif "calle" in title:
        df_tmp["street type"] = "calle"
        df_tmp["street"] = title.split(",")[0].split("calle")[-1]

    if "s/n" in title:
        df_tmp["street_number"] = "s/n"
    else:
        number = re.findall(r"\d+", title)
        if len(number) > 0:
            df_tmp["street_number"] = number[0]

    # print()
    # print(df_tmp.T)

    final_df = pd.concat([final_df, df_tmp], ignore_index=True, sort=False)

    # break

final_df.to_csv("data_hause/hause_info_handmade.csv", index=False, sep="\t")
