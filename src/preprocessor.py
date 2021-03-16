import config
import pandas as pd
import numpy as np
from sodapy import Socrata
pd.set_option('display.max_columns', None)


def rename_cols(df):
    df.index.rename('Transaction Number', inplace=True)
    df = df.rename(columns={'vendorid': 'Vendor Id'
                   , 'tpep_pickup_datetime': 'Pickup Datetime'
                   , 'tpep_dropoff_datetime': 'Dropoff Datetime'
                   , 'passenger_count': 'Passenger Count'
                   , 'trip_distance': 'Trip Distance'
                   , 'ratecodeid': 'Rate Code Id'
                   , 'store_and_fwd_flag': 'Store and Forward'
                   , 'pulocationid': 'Pick Up Location Id'
                   , 'dolocationid': 'Drop Off Location Id'
                   , 'payment_type': 'Payment Type'
                   , 'fare_amount': 'Fare Amount'
                   , 'extra': 'Extra'
                   , 'mta_tax': 'MTA Tax'
                   , 'tip_amount': 'Tip Amount'
                   , 'tolls_amount': 'Tolls Amount'
                   , 'improvement_surcharge': 'Improvement Surcharge'
                   , 'total_amount': 'Total Amount'
                   , 'congestion_surcharge': 'Congestion Surcharge'})
    return df


def make_numeric(df):
    cols = ['Pick Up Location Id', 'Drop Off Location Id', 'Passenger Count',
            'Trip Distance', 'Fare Amount', 'Extra', 'MTA Tax', 'Tip Amount',
            'Tolls Amount', 'Improvement Surcharge', 'Total Amount',
            'Congestion Surcharge']

    for col in cols:
        df[col] = pd.to_numeric(df[col])

    return df


def make_trip_speed(df):
    df['Pickup Datetime'] = pd.to_datetime(df['Pickup Datetime'])
    df['Dropoff Datetime'] = pd.to_datetime(df['Dropoff Datetime'])
    df['Trip Time (hrs)'] = ((df['Dropoff Datetime'] - df['Pickup Datetime'])/ np.timedelta64(1, 'h')).round(2)
    df['Trip Speed mph'] = (df['Trip Distance'] / df['Trip Time (hrs)']).round(2)
    return df


def replace_vals(df):
    df['Rate Code Id'] = df['Rate Code Id'].replace({'1': 'Standard rate',
                                                     '2': 'JFK',
                                                     '3': 'Newark',
                                                     '4': 'Nassau or Westchester',
                                                     '5': 'Negotiated fare',
                                                     '6': 'Group ride'})

    df['Payment Type'] = df['Payment Type'].replace({'1': 'Credit Card',
                                                     '2': 'Cash',
                                                     '3': 'No Charge',
                                                     '4': 'Dispute',
                                                     '5': 'Unknown',
                                                     '6': 'Voided_Trip'})

    df['Vendor Id'] = df['Vendor Id'].replace({'1': 'Creative Mobole',
                                               '2': 'VeriFone'})

    df['Store and Forward'] = df['Store and Forward'].replace({'Y': True,
                                                               'N': False})

    return df


def make_dummies(df):
    df = pd.get_dummies(df, columns=['Payment Type'],
                        dummy_na=True, drop_first=False)
    return df


def merge_dfs(df1, df2):

    df = df1.merge(df2, how='left',
                    left_on='Pick Up Location Id',
                    right_on='LocationID',
                    suffixes=('_Pick_Up', '_Pick_Up_Zone_name'))

    df = df.drop('LocationID', axis=1)

    df = df.merge(df2, how='left', 
                  left_on='Drop Off Location Id',
                  right_on='LocationID',
                  suffixes=('_PickUp', '_DropOff'))

    df = df.drop('LocationID', axis=1)

    return df


if __name__ == "__main__":

    # Authenticated client:
    client = Socrata('data.cityofnewyork.us',
                     config.api_key,
                     config.api_username,
                     config.api_password)

    # First 5000 results, returned as JSON from API / converted to 
    # Python list of dictionaries by sodapy
    results = client.get("2upf-qytp", limit=5000)

    # Convert to pandas DataFrame and get a smaller sample to try out functions
    results_df = pd.DataFrame.from_records(results)
    sample = results_df.sample(frac=.2)

    # clean the dataframe with a pipe
    taxidf_cleaned = (sample.
                      pipe(rename_cols).
                      pipe(make_numeric).
                      pipe(make_trip_speed).
                      pipe(replace_vals).
                      pipe(make_dummies))

    # read in taxi_zones csv to merge
    # sys.path.append("../data")
    taxi_zones = pd.read_csv('../data/taxi+_zone_lookup.csv')
    merge_dfs(taxidf_cleaned, taxi_zones)
