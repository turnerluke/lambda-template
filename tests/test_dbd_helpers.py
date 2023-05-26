import datetime as dt

import pandas as pd

from aws_helpers.dynamodb import dynamodb, get_entire_table, query_on_business_date


def test_init():
    assert dynamodb is not None


def test_get_entire_table():
    table = 'dining_options'
    data = get_entire_table(table)
    assert data is not None


def test_query_on_business_date():
    table = 'labor'
    start = dt.date(2022, 2, 1)
    end = start
    data = query_on_business_date(table, start, end)
    assert data is not None
    df = pd.DataFrame(data)
    assert '000-AUS-CK' in df['location'].unique()
