import os
import time
import json
import random

import requests
from bs4 import BeautifulSoup

os.system("clear")

url_base = "https://www.idealista.com/"
distritos = [
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
barrios = {
    "benalua-la-florida-babel-san-gabriel": [
        "benalua",
        "la-florida",
        "babel",
        "el-palmeral-urbanova-tabarca",
        "la-florida-portazgo",
        "alipark",
        "princesa-mercedes",
        "ciudad-de-asis",
        "san-gabriel",
    ],
    "campoamor-carolinas-altozano": [
        "carolinas-altas",
        "carolinas-bajas",
        "campoamor",
        "altozano",
        "benisaudet",
    ],
    "centro": [
        "ensanche-diputacion",
        "centro-tradicional",
        "mercado",
        "casco-historico-santa-cruz",
    ],
    "los-angeles-tombola-san-nicolas": [
        "los-angeles",
        "ciudad-de-asis-font-calent-el-bacarot",
        "tombola-rabasa",
        "san-agustin",
        "divina-pastora",
    ],
    "parque-avenidas-vistahermosa": [
        "vistahermosa",
        "garbinet-parque-de-las-avenidas",
        "nou-alacant",
    ],
    "pla-del-bon-repos-la-goleta-san-anton": [
        "pla-del-bon-repos-la-goteta",
        "raval-roig-virgen-del-socorro",
        "san-anton",
    ],
    "playa-de-san-juan-el-cabo": [
        "cabo-de-las-huertas",
        "playa-de-san-juan",
        "alicante-golf",
        "la-albufereta",
        "pau-5",
    ],
    "san-blas-pau": ["paus", "santo-domingo", "san-blas"],
    "villafranqueza-santa-faz-monegre": [
        "villafranqueza",
        "villahermosa-santa-faz",
        "valle-del-sol-el-portel",
    ],
    "virgen-del-remedio-juan-xxiii": [
        "virgen-del-remedio-parque-lo-morant",
        "colonia-requena-virgen-del-carmen",
        "juan-xxiii",
        "ciudad-elegida",
        "ciudad-jardin",
    ],
}
# casas_ids = {
#     "benalua": [],
#     "la-florida": [],
#     "babel": [],
#     "el-palmeral-urbanova-tabarca": [],
#     "la-florida-portazgo": [],
#     "alipark": [],
#     "princesa-mercedes": [],
#     "ciudad-de-asis": [],
#     "san-gabriel": [],
#     "carolinas-altas": [],
#     "carolinas-bajas": [],
#     "campoamor": [],
#     "altozano": [],
#     "benisaudet": [],
#     "ensanche-diputacion": [],
#     "centro-tradicional": [],
#     "mercado": [],
#     "casco-historico-santa-cruz": [],
#     "los-angeles": [],
#     "ciudad-de-asis-font-calent-el-bacarot": [],
#     "tombola-rabasa": [],
#     "san-agustin": [],
#     "divina-pastora": [],
#     "vistahermosa": [],
#     "garbinet-parque-de-las-avenidas": [],
#     "nou-alacant": [],
#     "pla-del-bon-repos-la-goteta": [],
#     "raval-roig-virgen-del-socorro": [],
#     "san-anton": [],
#     "cabo-de-las-huertas": [],
#     "playa-de-san-juan": [],
#     "alicante-golf": [],
#     "la-albufereta": [],
#     "pau-5": [],
#     "paus": [],
#     "santo-domingo": [],
#     "san-blas": [],
#     "villafranqueza": [],
#     "villahermosa-santa-faz": [],
#     "valle-del-sol-el-portel": [],
#     "virgen-del-remedio-parque-lo-morant": [],
#     "colonia-requena-virgen-del-carmen": [],
#     "juan-xxiii": [],
#     "ciudad-elegida": [],
#     "ciudad-jardin": [],
# }
headers = {
    # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.106 Safari/537.36',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "set-cookie": "_pxCaptcha=; Expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;",
}
casas_info = {}


# loop for 'distritos'
for distrito in distritos:
    print(f"Distrito: {distrito}")

    # there is an error with this district, we have to collect it manually.
    if distrito in ["pla-del-bon-repos-la-goleta-san-anton"]:
        continue

    # loop for 'barrios'
    for barrio in barrios[distrito]:
        print(f"\tBarrio: {barrio}")
        # hause_ids = []
        pages = True
        counter = 1

        # loop for 'pagina'
        while pages is True:
            secs = 2.0
            url = os.path.join(
                url_base,
                "venta-viviendas/alicante-alacant",
                distrito,
                barrio,
                f"pagina-{counter}.htm",
            )
            r = requests.get(url, headers=headers)
            html_page = BeautifulSoup(r.text, "html.parser")

            # all adds
            adds = html_page.select(".items-container article.item")
            for add in adds:
                # hause_ids.append(add.attrs["data-adid"])
                # ID
                single_id = add.attrs["data-adid"]
                # title
                title = add.select(".item-link")[0].text
                # price
                price = add.select(".item-price")[0].text
                # details
                details = add.select(".item-detail-char")[0]
                final_details = [d.text for d in details.select("span")]

                single_hause = {
                    "distrito": distrito,
                    "barrio": barrio,
                    "id": single_id,
                    "title": title,
                    "price": price,
                    "details": final_details,
                    "url": f"https://www.idealista.com/inmueble/{single_id}/",
                }
                casas_info.update({single_id: single_hause})

            next_page = html_page.select(".pagination .next")

            secs += random.random() + 4.0
            if len(next_page) > 0:
                print(
                    f"\t\tIteration {counter}: Waiting for {round(secs, 2)} seconds for the next iteration."
                )

                counter += 1
            elif counter >= 20:
                print(f"\t\tSomthing was wrong, going on with the next neighborhood.")
                pages = False
            else:
                print(f"\t\tIteration {counter}: This is the final page.")
                pages = False

            time.sleep(secs)

        # casas_ids[barrio] = hause_ids


# with open("data_hause/hause_ids.json", "w") as fp:
#     json.dump(casas_ids, fp, indent=4)

with open("data_hause/hause_info_summery.json", "w") as fp:
    json.dump(casas_info, fp, indent=4)
