import datetime as dt
import json
import decimal

import pandas as pd

from aws_helpers.dynamodb import query_on_business_date
from aws_helpers.s3 import save_df_as_csv
from labor.helpers import time_entries_and_start_dates_from_labor_data


if __name__ == '__main__':
    # Query Labor
    start = dt.date(2022, 2, 1)
    end = dt.date.today() - dt.timedelta(days=1)
    data = query_on_business_date("labor", start_date=start, end_date=end)
    labor, start_dates = time_entries_and_start_dates_from_labor_data(data)

    # Save to S3
    save_df_as_csv(labor, 'ziki-analytics-cleaned-datasets', 'time-entries.csv')
    save_df_as_csv(start_dates, 'ziki-analytics-cleaned-datasets', 'start-dates.csv')
