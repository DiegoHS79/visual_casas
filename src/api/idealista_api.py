import os
import time
import json
import random
import requests
from requests.auth import HTTPBasicAuth
from typing import Dict, Any

import pandas as pd
from dotenv import load_dotenv

os.system("clear")
# set your path enviromental file (your path)
load_dotenv("/home/oxcom/visual_casas/src/.env")

key = os.getenv("API_KEY")
secret = os.getenv("API_SECRET")


# * First: get the access token from idealista API
def get_token() -> str:
    oauth_url = "https://api.idealista.com/oauth/token"
    payload = {"grant_type": "client_credentials"}
    r = requests.post(oauth_url, auth=HTTPBasicAuth(key, secret), data=payload)
    token = json.loads(r.text)["access_token"]

    return token


def get_url(params: Dict[str, Any]) -> str:
    base_url = params["base_url"]
    country = params["country"]
    operation = params["operation"]
    max_items = params["max_items"]
    center = params["center"]
    distance = params["distance"]
    property_type = params["property_type"]
    language = params["language"]
    pagination = params["pagination"]

    url = f"{base_url}/{country}/search?operation={operation}&maxItems={max_items}&center={center}&distance={distance}"
    url += f"&propertyType={property_type}&language={language}&numPage={pagination}"
    # url += f"&order={order}&sort={sort}&maxPrice={maxprice}"

    return url


# basic params
params = {
    "base_url": "https://api.idealista.com/3.5",  # Base search url
    "country": "es",  # Search country (es, it, pt)
    "language": "es",  # Search language (es, it, pt, en, ca)
    "max_items": "50",  # Max items per call, the maximum set by Idealista is 50
    "operation": "sale",  # Kind of operation (sale, rent)
    "property_type": "homes",  # Type of property (homes, offices, premises, garages, bedrooms)
    "center": "38.34517,-0.48149",  # Coordinates of the search center (Alicante)
    "distance": "25000",  # Max distance from the center [m]
    # "sort": "desc",  # How to sort the found items
    # "order": "priceDown",  # Order of the listings, consult documentation for all the available orders
    # "maxprice": "750",  # Max price of the listings
    # "bankOffer": "false",  # If the owner is a bank
}

# connexion
i = 1
while True:
    params.update({"pagination": i})
    url = get_url(params=params)

    if i == 1:
        token = get_token()
        headers = {"Authorization": f"Bearer {token}"}

    content = requests.post(url, headers=headers)
    result = json.loads(content.text)

    # print(json.dumps(result, indent=4))
    data = result["elementList"]
    if i == 1:
        df = pd.DataFrame.from_dict(data)
    else:
        df = pd.concat([df, pd.DataFrame.from_dict(data)])

    total_pages = result["totalPages"]
    print(f"Iteration {i} of {total_pages}")
    if i < total_pages:
        i += 1
    else:
        break


df.to_csv("data/data_hauses.csv", index=False, sep="\t")
