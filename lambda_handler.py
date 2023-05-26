import config.settings

import json

import boto3

from slackbot.messages import send_message_to_slack_channel
from orders.helpers import sales_and_payments_from_raw_order_data
from labor.helpers import time_entries_and_start_dates_from_labor_data
from aws_helpers.s3 import get_csv_as_df

# Get deserializer to change DynamoDB format to JSON
boto3.resource('dynamodb')
deserializer = boto3.dynamodb.types.TypeDeserializer()


def handler(event, context):
    event_txt = json.dumps(event, sort_keys=True, indent=4)
    send_message_to_slack_channel(event_txt)
    table_name = event['Records'][0]['eventSourceARN'].split('/')[1]

    new_data = []

    for record in event["Records"]:
        assert record['eventSourceARN'].split('/')[1] == table_name, \
            f"Event source ARN {record['eventSourceARN']} does not match table name {table_name}."

        if record['eventName'] == 'REMOVE':
            old_record = record['dynamodb']['OldImage']
            assert False, \
                f"DynamoDB stream event deleted a record. This shouldn't happen.\n" \
                f"Table: {table_name}\n" \
                f"Record Deleted:\n{old_record}"

        else:
            new_record = record['dynamodb']['NewImage']
            new_record = {k: deserializer.deserialize(v) for k, v in new_record.items()}
            new_data.append(new_record)

    if table_name == 'orders':
        sales = get_csv_as_df(config.settings.S3_BUCKET, 'sales.csv')
        payments = get_csv_as_df(config.settings.S3_BUCKET, 'payments.csv')
        new_sales, new_payments = sales_and_payments_from_raw_order_data(new_data)
        pass
    elif table_name == 'labor':
        time_entries = get_csv_as_df(config.settings.S3_BUCKET, 'time_entries.csv')
        start_dates = get_csv_as_df(config.settings.S3_BUCKET, 'start_dates.csv')
        new_time_entries, _ = time_entries_and_start_dates_from_labor_data(new_data)
        for new_time_entries

