import requests
from requests.structures import CaseInsensitiveDict
import numpy as np
import pandas as pd
from urllib.parse import quote
import streamlit as st

# api_key = pd.read_csv("geoapi_key.csv")['API key'][0]
api_key = st.secrets['api_key']

def coordinates_from_address(address_search_text):
    """
    Geographical coordinates, corresponding to the entered address information.
    Interpunction can be used, but it is not quite important.
    Argument:
        address_search_text: string
    Output:
        The first matched lon/lat pair as a list
    """
    address_search_text_conv = quote(address_search_text.encode('utf8'))
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    base_url = "https://api.geoapify.com/v1/geocode/search?text="
    url = base_url+address_search_text_conv+"&apiKey="+api_key

    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        features = resp.json()['features']
        coordinates = [[np.NaN, np.NaN]]
        if len(features)>0:
            coordinates = [features[i]['geometry']['coordinates'] for i in range(len(features))]
            # A list of lon/lat pairs

    return coordinates[0]

# Examples
# print("Multiple matches")
# print(coordinates_from_address("Berliner str. 3"))

# print("\nUnique match")
# print(coordinates_from_address("Berliner 3 Hagen"))

# print("\nNo matches")
# print(coordinates_from_address("Berliner 3, Cannes"))
