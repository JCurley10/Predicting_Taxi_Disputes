import requests
import json
import pandas as pd
from pandas import json_normalize
from requests.exceptions import HTTPError
from requests.auth import HTTPBasicAuth
from getpass import getpass

pd.set_option('display.max_columns', None)

response = requests.get("https://data.cityofnewyork.us/resource/2upf-qytp.json", auth=HTTPBasicAuth('Jessicalcurley10@gmail.com', 'i@CB.hADCq7'))

jason = response.json()

df = json_normalize(jason)