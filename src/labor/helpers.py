import json
import datetime as dt

import pandas as pd

from aws_helpers.dynamodb import get_entire_table


def time_entries_and_start_dates_from_labor_data(data):
    labor = pd.DataFrame(data)

    # Remove deleted
    labor = labor.loc[~labor['deleted']]

    # Sanity checks
    assert labor['deletedDate'].isna().all(), 'Deleted entries remain'
    assert (~labor['deleted']).all(), 'Deleted entries remain'
    assert labor['shiftReference'].isna().all(), 'Shift reference showed up.'

    # Trim to relevant columns
    labor = labor[
        ['employeeReference', 'jobReference', 'inDate', 'outDate', 'businessDate', 'hourlyWage', 'regularHours',
         'overtimeHours', 'guid']]

    # Unpack employee and job guids from reference objects
    labor['employeeGuid'] = labor['employeeReference'].apply(pd.Series)['guid']
    labor['jobGuid'] = labor['jobReference'].apply(pd.Series)['guid']
    labor = labor.drop(columns=['employeeReference', 'jobReference'])

    # Get employee info
    employees = get_entire_table('employees')
    employees = pd.DataFrame(employees)
    employees = employees[
        ['guid', 'v2EmployeeGuid', 'chosenName', 'firstName', 'lastName', 'wageOverrides', 'jobReferences']]

    # Merge employee info
    labor = labor.merge(
        employees[['guid', 'chosenName', 'firstName', 'lastName']],
        how='left',
        left_on='employeeGuid',
        right_on='guid',
        suffixes=('TimeEntry', 'Employee')
    )
    labor = labor.drop(columns=['guidEmployee'])

    # Calculate pay
    labor['regularPay'] = labor['regularHours'].astype(float) * labor['hourlyWage'].astype(float)
    labor['overtimePay'] = labor['overtimeHours'].astype(float) * labor['hourlyWage'].astype(float) * 1.5

    # Business date integer to datetime
    labor['businessDate'] = pd.to_datetime(labor['businessDate'], format='%Y%m%d')

    # Get start dates for each employee
    start_dates = labor[
        ['employeeGuid', 'businessDate']
    ].groupby('employeeGuid').min().reset_index().rename(
        columns={'businessDate': 'startDate'}
    )

    # Get start dates for each employee
    labor = labor.merge(
        start_dates,
        how='left',
        on='employeeGuid'
    )

    # Denote training entries
    labor['isTraining'] = labor['businessDate'] < (labor['startDate'] + dt.timedelta(days=14))
    labor = labor.drop(columns=['startDate'])
    return labor, start_dates