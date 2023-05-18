import gzip
import json

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
