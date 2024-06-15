import json
from datetime import datetime
import pandas as pd

def read_data(file_path):
    """
    Read the JSON data

    Parameters:
    file_path: str

    Returns:
    data: dict
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data

def convert_to_datetime(date):
    """
    Convert the date to a datetime object

    Parameters:
    date: str

    Returns:
    datetime object
    """
    return datetime.strptime(date, "%b-%y")

def create_df(data):
    """
    Create a DataFrame from the JSON data

    Parameters:
    data: dict

    Returns:
    df: pd.DataFrame
    """
    data_list = []

    for group, tasks in data.items():
        for task, dates in tasks.items():
            data_list.append(
                [
                    group,
                    task,
                    convert_to_datetime(dates["begin"]),
                    dates["duration"],
                ]
            )

    df = pd.DataFrame(data_list, columns=["Task Group", "Task", "Begin", "Duration"])
    return df

def calculate_week_number(df):
    """
    Calculate the week number of the tasks

    Parameters:
    df: pd.DataFrame

    Returns:
    df: pd.DataFrame
    """
    df["Week_Number"] = df["Begin"].dt.isocalendar().week
    return df


def calculate_end_date(df):
    """
    Calculate the end date of the tasks

    Parameters:
    df: pd.DataFrame

    Returns:
    df: pd.DataFrame
    """
    df["End"] = df["Begin"] + pd.to_timedelta((df["Duration"]*4), unit="W")
    return df

def modify_df_from_interuptions(df_updated, df_interuptions):
    """
    Changes the dates of tasks that appear after the interruption date.

    Parameters:
    df_updated: pd.DataFrame
    df_interuptions: pd.DataFrame

    Returns:
    df_updated: pd.DataFrame
    """
    for _, interruption in df_interuptions.iterrows():
        # Calculate the interruption duration in days
        interruption_duration_days = interruption['Duration'] * 30  # Approximate month duration as 30 days

        # Condition 1: If the task ends after the interruption starts
        condition1 = df_updated['End'] > interruption['Begin']

        # Condition 2: If the task begins and ends after the interruption starts
        condition2 = (df_updated['Begin'] > interruption['Begin']) & (df_updated['End'] > interruption['Begin'])

        # Adjust only the end dates for tasks that begin before and end after the interruption starts
        df_updated.loc[condition1 & ~condition2, 'End'] += pd.to_timedelta(interruption_duration_days, unit='D')

        # Adjust both the begin and end dates for tasks that begin and end after the interruption starts
        df_updated.loc[condition2, 'Begin'] += pd.to_timedelta(interruption_duration_days, unit='D')
        df_updated.loc[condition2, 'End'] += pd.to_timedelta(interruption_duration_days, unit='D')

    return df_updated


def load_data(file_path):
    """
    Load the data from the JSON file

    Parameters:
    file_path: str

    Returns:
    df: pd.DataFrame
    """
    data = read_data(file_path)
    df = create_df(data)
    df = calculate_week_number(df)
    df = calculate_end_date(df)
    return df