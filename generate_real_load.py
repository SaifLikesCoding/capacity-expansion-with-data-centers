import requests
import json as js
import pandas as pd

api_key = "lJ9R6IRAMmNrP38jOIdpxmkAvWJmjgrCfN5K0igN"
url = f"https://api.eia.gov/v2/electricity/rto/region-data/data/?api_key={api_key}&frequency=hourly&data[0]=value&facets[type][]=D&facets[respondent][]=CISO&sort[0][column]=period&sort[0][direction]=asc&length=240"
output_cali = requests.get(url)
data  = output_cali.json()
values = [entry["value"] for entry in data["response"]["data"]]
df = pd.DataFrame ({"Load_synthetic": values})
df.to_csv ("wecc_load.csv",index = False)
