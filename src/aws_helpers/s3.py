import os
import gzip
import json
import io

import pandas as pd
import boto3

s3 = boto3.client('s3')


def read_from_s3(bucket_name, file_name):
    # read the file
    obj = s3.get_object(Bucket=bucket_name, Key=file_name)
    file_content = obj['Body'].read()

    # Check if the file is compressed in Gzip format
    if is_gzip(file_content):
        # If the file is compressed in Gzip format, decompress it
        file_content = gzip.decompress(file_content)

    # Decode the file content as utf-8
    decoded_content = file_content.decode('utf-8')

    return decoded_content.strip()


def is_gzip(file_content):
    """
    Check if the file is compressed in Gzip format.
    :param file_content:
    :return:
    """
    return file_content[:2] == b'\x1f\x8b'


def write_to_s3(bucket_name, file_name, data):
    if type(data) != str:
        data = json.dumps(data)
    # upload the file
    s3.put_object(Body=data, Bucket=bucket_name, Key=file_name)


def save_df_as_csv(df, bucket_name, csv_path):
    """
    Save a Pandas DataFrame as a CSV file in S3.
    :param df: Pandas DataFrame
    :param bucket_name: S3 bucket name
    :param csv_path: S3 path to the CSV file
    :return:
    """
    # Save the DataFrame as a local CSV file
    local_csv_path = 'temp.csv'
    df.to_csv(local_csv_path, index=False)

    # Upload the local CSV file to S3
    s3.upload_file(local_csv_path, bucket_name, csv_path)

    os.remove(local_csv_path)


def get_csv_as_df(bucket_name, csv_path):
    """
    Read a CSV file from S3 and return a Pandas DataFrame.
    :param bucket_name: S3 bucket name
    :param csv_path: S3 path to the CSV file
    :return: Pandas DataFrame
    """
    obj = s3.get_object(Bucket=bucket_name, Key=csv_path)
    df = pd.read_csv(io.BytesIO(obj['Body'].read()))

    return df


if __name__ == '__main__':
    df = get_csv_as_df('ziki-analytics-cleaned-datasets', 'sales.csv')
    print(df)