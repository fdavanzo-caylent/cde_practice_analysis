import pandas as pd

# Configure logging
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def analyze(issues_df):
    issues_df['status_change_date'] = pd.to_datetime(issues_df['status_change_date'])
    cfd_data = issues_df.groupby(['status_to', issues_df['status_change_date'].dt.to_period('D')]).size().unstack().fillna(0).cumsum(axis=1)
    return cfd_data


