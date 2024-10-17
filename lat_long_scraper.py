import requests
import pandas as pd
from bs4 import BeautifulSoup

# Base url for google search
BASE_URL = "https://www.google.com/search?q="

# headers to simulate a real browser visit
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

# function to scrape latitude and longitude
def get_coordinates(sector):
    search_term = f"sector {sector} gurgaon longitude & latitude"
    response = requests.get(BASE_URL,headers=headers)

    if response.status_code==200:
        soup = BeautifulSoup(response.content,'html.parser')
        coordinates_div = soup.find("div",class_="wvKXQ",style = "color:#FFEED9")
        if coordinates_div:
            return coordinates_div.text
    return None

# create a dataframe
df = pd.DataFrame(columns=["Sector","Coordinates"])
# Iterate over sectors and fetch coordinates
for sector in range(1,116):
    coordinates = get_coordinates(sector)
    df = df._append({"Sector":f"Sector {sector}","Coordinates":coordinates},ignore_index=True)

# save dataframe
df.to_csv("gurgaon_sectors_coordinates.csv")

