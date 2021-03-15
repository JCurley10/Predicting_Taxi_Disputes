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

cols = ['vendorid', 'tpep_pickup_datetime', 'tpep_dropoff_datetime',
       'passenger_count', 'trip_distance', 'ratecodeid', 'store_and_fwd_flag',
       'pulocationid', 'dolocationid', 'payment_type', 'fare_amount', 'extra',
       'mta_tax', 'tip_amount', 'tolls_amount', 'improvement_surcharge',
       'total_amount', 'congestion_surcharge']

# reindex so each row is a trip instance
# match taxizone with zipcode 
# datetimes are datetimes
# engineer feature: mph (time / distance )
# one hot encode the payment types 
# one hot encode Extra 
# convert all numeric strings to floats/numerics