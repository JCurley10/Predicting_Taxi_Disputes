import boto3
import os
import pandas as pd

def print_s3_contents_boto3(connection):
    for bucket in connection.buckets.all():
        for key in bucket.objects.all():
            print(key.key)

def load_csv_from_s3(bucketname, filename, n_rows=300):
    """
    Input:
        bucketname (str): Name of bucket that file is stored in
        filename (str): Name of csv within bucket (ex: "cool_data.csv")
    Output:
        pandas dataframe of csv (assuming no read_csv arguments are needed)
    """

    boto_object = boto3_client.get_object(Bucket=bucketname, Key=filename)
    return pd.read_csv(boto_object['Body'], nrows=n_rows)


if __name__ == "__main__":
    boto3_client = boto3.client('s3')
    boto3_connection = boto3.resource('s3')

    username = os.environ['USER']

    bucketname = 'nyc-2019-yellow-taxi'
    # clean_bucketname = 'nyc-2019-yellow-taxi-processed'

    filename = '2019_Yellow_Taxi_Trip_Data.csv'

    # TODO: run the preprocessor over the csv and push it up to an S3 that can be pulled
    