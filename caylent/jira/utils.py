import pandas as pd

# Configure logging
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def process_closed_dates(df):
    df['status_change_date'] = pd.to_datetime(df['status_change_date'])
    closed_df = df[df['status_to'].isin(['Closed', 'Done', 'Resolved'])]  # Add other equivalent statuses as needed
    
    # Get the earliest closure date per issue
    closed_dates = closed_df.groupby('issue_key')['status_change_date'].min().reset_index()
    closed_dates.rename(columns={'status_change_date': 'closed_date'}, inplace=True)
    df = df.merge(closed_dates, on='issue_key', how='left')

    return df