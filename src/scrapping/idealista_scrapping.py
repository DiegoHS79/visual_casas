import os
import time
import random
from datetime import date

import requests
import pandas as pd
from bs4 import BeautifulSoup

os.system("clear")

url_base = "https://www.idealista.com/sala-de-prensa/informes-precio-vivienda/venta/comunitat-valenciana/alicante-alacant/alicante-alacant/"
barrios = [
    "benalua-la-florida-babel-san-gabriel",
    "campoamor-carolinas-altozano",
    "centro",
    "los-angeles-tombola-san-nicolas",
    "parque-avenidas-vistahermosa",
    "pla-del-bon-repos-la-goleta-san-anton",
    "playa-de-san-juan-el-cabo",
    "san-blas-pau",
    "villafranqueza-santa-faz-monegre",
    "virgen-del-remedio-juan-xxiii",
]
headers = {
    # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.106 Safari/537.36',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "set-cookie": "_pxCaptcha=; Expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;",
}

for barrio in barrios:
    secs = 0.5
    print(f"Getting data from {barrio}")
    r = requests.get(url_base + barrio + "/historico/", headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    # header
    header = soup.select("table thead tr th *")
    columns = []
    for head in header:
        columns.append(head.text)

    # body
    file_container = soup.select("table tbody tr")

    # loop on every month
    all_rows = []
    for row in file_container:
        all_row = row.select("td")

        # loop on every row element
        single_row = []
        for element in all_row:
            single_row.append(element.attrs["data-sortable"])

        all_rows.append(single_row)

    df = pd.DataFrame(all_rows, columns=columns)
    df.to_csv(f"data_temporal/{barrio.replace('-', '_')}.csv", sep="\t", index=False)

    secs += random.random()
    print(f"WARNING: Waiting for {secs} seconds for the next scrapping.\n")
    time.sleep(secs)
