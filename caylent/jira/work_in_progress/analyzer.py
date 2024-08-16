import pandas as pd
from config.config import WIP_ALL_ISSUE_STATUSES

# Configure logging
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def analyze(issues_df):
    issues_df['status_change_datetime'] = pd.to_datetime(issues_df['status_change_date'])
    issues_df_sorted = issues_df.sort_values(by=['issue_key', 'status_change_datetime'])

    # Remove duplicate status changes, keeping only the last change per day for each issue
    issues_df_sorted['status_change_date'] = issues_df_sorted['status_change_datetime'].dt.date
    filtered_df = issues_df_sorted.drop_duplicates(subset=['issue_key', 'status_change_date'], keep='last')
    # filtered_df = filtered_df.drop(columns=['status_change_datetime'])

    # Create a time series DataFrame
    date_range = pd.date_range(start=filtered_df['status_change_date'].min(), end=filtered_df['status_change_date'].max()).date
    time_series_df = pd.DataFrame(index=date_range, columns=WIP_ALL_ISSUE_STATUSES).fillna(0)

    # Initialize a dictionary to keep track of the current status of each issue
    current_status = {}
    
    # Update the time series DataFrame with the number of issues in each status for each day
    for date in date_range:
        for status in WIP_ALL_ISSUE_STATUSES:
            # Set the count to zero for each status for the current date
            time_series_df.loc[date, status] = 0

        # Update the current status of each issue
        for _, row in filtered_df.iterrows():
            issue_key = row['issue_key']
            change_date = row['status_change_date']
            if change_date == date:
                current_status[issue_key] = row['status_to']

        # Count the number of issues in each relevant status
        for status in WIP_ALL_ISSUE_STATUSES:
            time_series_df.loc[date, status] = sum(1 for v in current_status.values() if v == status)

    time_series_df['status_change_date'] = time_series_df.index
    return time_series_df


