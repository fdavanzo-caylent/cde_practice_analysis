import pandas as pd

# Configure logging
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def analyze(issues_df):
    issues_df['created'] = pd.to_datetime(issues_df['created'])
    issues_df['cycle_time'] = (issues_df['closed_date'] - issues_df['created']).dt.total_seconds() / 86400  # Convert to days
    return issues_df[['issue_key', 'created', 'closed_date', 'cycle_time']]


