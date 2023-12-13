import os
import re
import time
import json
import random

import requests
from requests import Request, Session
from bs4 import BeautifulSoup

os.system("clear")

url_base = "https://www.idealista.com/inmueble"


# https://www.useragents.me/
ua = [
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Safari/605.1.1",
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.3",
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.1",
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.1",
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3",
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.",
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.",
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.",
    # "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.3",
    # "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.",
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.3",
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Herring/90.1.9310.1",
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.",
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.4",
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
]
headers = {
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    # "Accept-Encoding": "gzip, deflate, br",
    # "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    # "Cache-Control": "no-cache",
    # "Connection": "keep-alive",
    # "Pragma": "no-cache",
    # "Sec-Ch-Ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    # "Sec-Fetch-Dest": "document",
    # "Sec-Fetch-Mode": "navigate",
    # "Sec-Fetch-Site": "none",
    # "Sec-Fetch-User": "?1",
    # "Upgrade-Insecure-Requests": "1",
    # "Set-Cookie": "_pxCaptcha=; Expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;",
    "User-Agent": random.choice(ua),
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

    for hause_id in ids_list:
        hause_info = {"barrio": barrio}
        secs = 2.0 + random.random() * 5.0

        if hause_id in list(all_hauses_info.keys()):
            print(f"\tHause ID {hause_id} already in our database, continue.")
            continue
        else:
            print(f"\tExtracting the data for Hause ID: {hause_id}.")

        url = os.path.join(url_base, hause_id)
        hause_info.update({"hause_id": hause_id, "url": url})

        # ! alt. 1
        # with requests.Session() as s:
        #     r = s.get(url, headers=headers)

        # ! alt 2
        r = requests.get(url, headers=headers)

        # ! alt 3
        # resp = Request("GET", url, headers=headers)
        # with requests.Session() as s:
        #     r = s.send(
        #         resp.prepare(),
        #         # stream=stream,
        #         # verify=verify,
        #         # proxies=proxies,
        #         # cert=cert,
        #         # timeout=timeout,
        #     )
        print(r.headers)
        import sys

        sys.exit("")
        if "User-Agent" not in list(r.headers.keys()):
            print(headers)
            print("*" * 20)
            for a in r.headers.items():
                print(a)
            print(f"\tERROR: No 'User-Agent' in connection.")
            time.sleep(secs)
            continue

        # check for the same url (sometimes changes)
        returned_id = re.findall(r"\d+", r.url)[0]
        if hause_id != returned_id:
            print(
                f"\tHause ID: {hause_id} is not the same as the returned ID: {returned_id}"
            )
            time.sleep(secs)
            continue

        html_page = BeautifulSoup(r.text, "html.parser")

        # precio
        html_price = html_page.select(".detail-content-wrapper .info-data-price")
        price = html_price[0].text
        hause_info.update({"price": price})

        # text
        html_text = html_page.select(
            ".detail-content-wrapper .commentsContainer .comment p"
        )
        if len(html_text) > 0:
            text = html_text[0].text
            hause_info.update({"text": text})
        else:
            hause_info.update({"text": "NULL"})

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
        time.sleep(secs)

        # save in every step to avoid on starting from the beginning
        with open("data_hause/all_data_hauses.json", "w") as fp:
            json.dump(all_hauses_info, fp, indent=4)
