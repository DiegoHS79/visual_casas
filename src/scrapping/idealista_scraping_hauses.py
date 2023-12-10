import os
import time
import json
import random

import requests
from bs4 import BeautifulSoup

os.system("clear")

url_base = "https://www.idealista.com/inmueble"
headers = {
    # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.106 Safari/537.36',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "set-cookie": "_pxCaptcha=; Expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;",
}

with open("data_hause/hause_ids.json", "r") as fp:
    hauses_ids = json.load(fp)

try:
    with open("data_hause/all_data_hauses.json", "r") as fp:
        all_hauses_info = json.load(fp)
except FileNotFoundError:
    all_hauses_info = {}

for barrio in list(hauses_ids.keys()):
    print(f"Barrio: {barrio}")

    ids_list = hauses_ids[barrio]

    hause_info = {"barrio": barrio}
    for hause_id in ids_list:
        if hause_id in list(all_hauses_info.keys()):
            print(f"\tHause ID {hause_id} already in our database, continue.")
            continue
        else:
            print(f"\tExtracting the data for Hause ID: {hause_id}.")

        url = os.path.join(url_base, hause_id)
        hause_info.update({"hause_id": hause_id, "url": url})

        r = requests.get(url, headers=headers)
        html_page = BeautifulSoup(r.text, "html.parser")

        # precio
        html_price = html_page.select(".detail-content-wrapper .info-data-price")
        price = html_price[0].text
        hause_info.update({"price": price})

        # text
        html_text = html_page.select(
            ".detail-content-wrapper .commentsContainer .comment p"
        )
        text = html_text[0].text
        hause_info.update({"text": text})

        # details
        details = []
        html_details = html_page.select(".detail-content-wrapper .details-box li")
        for detail in html_details:
            if "span" in str(detail):
                continue
            details.append(detail.text)

        html_details2 = html_page.select(".detail-content-wrapper .details-box li span")
        for detail in html_details2:
            if "title" in str(detail):
                details.append(detail.attrs["title"])
            details.append(detail.text)
        hause_info.update({"details": details})

        # place
        html_place = html_page.select(".ide-box-detail .clearfix ul li.header-map-list")
        location_info = []
        for info in html_place:
            location_info.append(info.text)
        hause_info.update({"location_info": location_info})

        all_hauses_info.update({hause_id: hause_info})

        # waiting time to avoid being banned
        secs = 2.0 + random.random()
        time.sleep(secs)

        # save in every step to avoid on starting from the beginning
        with open("data_hause/all_data_hauses.json", "w") as fp:
            json.dump(all_hauses_info, fp, indent=4)

    break
