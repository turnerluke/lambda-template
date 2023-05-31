import config.settings

import json
import traceback

import pandas as pd
import boto3

from slackbot.messages import send_message_to_slack_channel
from orders.helpers import sales_and_payments_from_raw_order_data
from labor.helpers import time_entries_and_start_dates_from_labor_data
from aws_helpers.s3 import get_csv_as_df, save_df_as_csv

# Get deserializer to change DynamoDB format to JSON
boto3.resource('dynamodb')
deserializer = boto3.dynamodb.types.TypeDeserializer()


def remove_duplicates(lst: list[dict]) -> list[dict]:
    """Removes duplicate dictionaries from a list of dictionaries."""
    seen = set()
    new_lst = []
    for d in lst:
        key = d['guid']
        if key not in seen:
            seen.add(key)
            new_lst.append(d)
    return new_lst


def handler(event, context):
    try:
        msg = '=' * 50 + '\n'
        table_name = event['Records'][0]['eventSourceARN'].split('/')[1]
        print(table_name)
        msg += f"DynamoDB Table Update: {table_name}\n"

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

        # Remove duplicates
        new_data = remove_duplicates(new_data)

        if table_name == 'orders':
            sales = get_csv_as_df(config.settings.S3_BUCKET, 'sales.csv')
            payments = get_csv_as_df(config.settings.S3_BUCKET, 'payments.csv')
            new_sales, new_payments = sales_and_payments_from_raw_order_data(new_data)
            # Process sales
            start_num_rows = len(sales)
            # Remove repeated orders
            sales = sales.loc[
                ~sales['guid'].isin(new_sales['guid'].unique())
            ]
            end_num_rows = len(sales)
            dropped_rows = start_num_rows - end_num_rows
            new_rows = len(new_sales)
            # Append new data
            sales = pd.concat([sales, new_sales], axis=0, ignore_index=True)
            sales['businessDate'] = pd.to_datetime(sales['businessDate']).dt.date

            msg += f"Rows dropped in sales table: {dropped_rows}\n"
            msg += f"Rows added to sales table: {new_rows}\n"

            # Process payments
            start_num_rows = len(payments)
            # Remove repeated payments
            payments = payments.loc[
                ~payments['guid'].isin(new_payments['guid'].unique())
            ]
            end_num_rows = len(payments)
            dropped_rows = start_num_rows - end_num_rows
            new_rows = len(new_payments)
            # Append new data
            payments = pd.concat([payments, new_payments], axis=0, ignore_index=True)

            msg += f"Rows dropped in payments table: {dropped_rows}\n"
            msg += f"Rows added to payments table: {new_rows}\n"

            # Save to S3
            save_df_as_csv(sales, config.settings.S3_BUCKET, 'sales.csv')
            save_df_as_csv(payments, config.settings.S3_BUCKET, 'payments.csv')

        elif table_name == 'labor':
            time_entries = get_csv_as_df(config.settings.S3_BUCKET, 'time-entries.csv')
            start_dates = get_csv_as_df(config.settings.S3_BUCKET, 'start-dates.csv')
            new_time_entries, new_start_dates = time_entries_and_start_dates_from_labor_data(new_data, start_dates)

            # Process time entries
            start_num_rows = len(time_entries)
            # Remove repeated entires
            time_entries = time_entries.loc[
                ~time_entries['guidTimeEntry'].isin(new_time_entries['guidTimeEntry'].unique())
            ]
            end_num_rows = len(time_entries)
            dropped_rows = start_num_rows - end_num_rows
            new_rows = len(new_time_entries)
            # Append new data
            time_entries = pd.concat([time_entries, new_time_entries], axis=0, ignore_index=True)
            time_entries['businessDate'] = pd.to_datetime(time_entries['businessDate']).dt.date

            msg += f"Rows dropped in time entries table: {dropped_rows}\n"
            msg += f"Rows added to time entries table: {new_rows}\n"

            # Process start dates
            start_entries = len(start_dates)
            end_entries = len(new_start_dates)
            msg += f"Rows added to start-dates table: {end_entries - start_entries}\n"

            # Save to S3
            save_df_as_csv(time_entries, config.settings.S3_BUCKET, 'time-entries.csv')
            save_df_as_csv(start_dates, config.settings.S3_BUCKET, 'start-dates.csv')
        else:
            raise ValueError(f"Table name {table_name} not recognized.")

        msg += '=' * 50
        send_message_to_slack_channel(msg)
        print(msg)

    except Exception as e:
        send_message_to_slack_channel(
            f"<@U0470Q1MJM8>\nError occurred:\n```{e}```\nTraceback:\n```{traceback.format_exc()}```"
        )
        print(f"<@U0470Q1MJM8>\nError occurred:\n```{e}```\nTraceback:\n```{traceback.format_exc()}```")
        raise e

