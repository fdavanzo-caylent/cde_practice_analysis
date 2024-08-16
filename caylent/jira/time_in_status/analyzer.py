import pandas as pd

# Configure logging
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def analyze(issues_df, status):
    issues_df['status_change_date'] = pd.to_datetime(issues_df['status_change_date'])
    issues_df = issues_df.sort_values(by=['issue_key', 'status_change_date'])
    issues_df['time_in_status'] = issues_df.groupby('issue_key')['status_change_date'].diff().shift(-1)
    
    status_df = issues_df[issues_df['status_to'] == status]
    total_time_in_status = status_df.groupby('issue_key')['time_in_status'].sum().reset_index()
    total_time_in_status['time_in_status'] = total_time_in_status['time_in_status'].dt.total_seconds() / 3600  # Convert to hours
    total_time_in_status['time_in_status'] = total_time_in_status['time_in_status'].round(2)
    
    return total_time_in_status


