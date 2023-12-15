import os
import time
import json
import requests
from requests.auth import HTTPBasicAuth

from dotenv import load_dotenv

os.system("clear")
# set your path enviromental file
load_dotenv("/Users/diegohs/Documents/MASTER/visual_casas/src/.env")

key = os.getenv("API_KEY")
secret = os.getenv("API_SECRET")

# * First: get the access token from idealista API
oauth_url = "https://api.idealista.com/oauth/token"
payload = {"grant_type": "client_credentials"}
r = requests.post(oauth_url, auth=HTTPBasicAuth(key, secret), data=payload)
token = json.loads(r.text)["access_token"]

# basic params
base_url = "https://api.idealista.com/3.5/"  # Base search url
country = "es"  # Search country (es, it, pt)
language = "es"  # Search language (es, it, pt, en, ca)
max_items = "50"  # Max items per call, the maximum set by Idealista is 50
operation = "sale"  # Kind of operation (sale, rent)
property_type = (
    "homes"  # Type of property (homes, offices, premises, garages, bedrooms)
)
order = "priceDown"  # Order of the listings, consult documentation for all the available orders
center = "38.34517,-0.48149"  # Coordinates of the search center
distance = "60000"  # Max distance from the center
sort = "desc"  # How to sort the found items
# bankOffer = "false"  # If the owner is a bank
# maxprice = "750"  # Max price of the listings

url = (
    base_url
    + country
    + "/search?operation="
    + operation
    + "&maxItems="
    + max_items
    + "&order="
    + order
    + "&center="
    + center
    + "&distance="
    + distance
    + "&propertyType="
    + property_type
    + "&sort="
    + sort
    + "&numPage=%s"
    # + "&maxPrice="
    # + maxprice
    + "&language="
    + language
)

# connexion
headers = {"Authorization": "Bearer " + token}
content = requests.post(url, headers=headers)
result = json.loads(content.text)

print(result)
