import pandas as pd

# Configure logging
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def analyze(issues_df):
    issues_df['closed_date'] = pd.to_datetime(issues_df['closed_date'])
    issues_df['week'] = issues_df['closed_date'].dt.to_period('W')
    throughput = issues_df.groupby('week').size().reset_index(name='throughput')
    return throughput


