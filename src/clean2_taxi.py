import pandas as pd
from sodapy import Socrata

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
# client = Socrata("data.cityofnewyork.us", None)

# Example authenticated client (needed for non-public datasets):
client = Socrata('data.cityofnewyork.us',
                 '83oe7nE4U1koOitHpKvyhpIqP',
                 "Jessicalcurley10@gmail.com",
                 "i@CB.hADCq7")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("2upf-qytp", limit=500000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)