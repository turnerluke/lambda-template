import datetime as dt
import json
import decimal

import pandas as pd

from aws_helpers.dynamodb import query_on_business_date
from aws_helpers.s3 import save_df_as_csv

from orders.helpers import sales_and_payments_from_raw_order_data


if __name__ == '__main__':
    # Query Orders
    start = dt.date(2022, 2, 1)
    end = dt.date.today() - dt.timedelta(days=1)
    data = query_on_business_date("orders", start_date=start, end_date=end)

    sales, payments = sales_and_payments_from_raw_order_data(data)

    # Save to S3
    save_df_as_csv(sales, 'ziki-analytics-cleaned-datasets', 'sales.csv')
    save_df_as_csv(payments, 'ziki-analytics-cleaned-datasets', 'payments.csv')
