import pandas as pd
from caylent.jira.time_in_status.analyzer import analyze
from caylent.jira.time_in_status.visualizer import visualize
from config.config import OUTPUT_JIRA_ANALYSIS_FOLDER, FILENAME_TIME_IN_STATUS_CSV, FILENAME_TIME_IN_STATUS_CHART

# Configure logging
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# TODO: At least for blocked statuses, I think we will want to eventually check for a label like "blocked_by_client" 
# or something like that and then we can output a table noting the jira slips blocked by client or us and the amount
# of blocked time.
# The labels exist as an array in the data frame issues_df['labels']
# Not sure if we get multiple records as the labels change, need to test

def generate(issues_df, status):
    # generate the dataframe with analysis
    status_df = analyze(issues_df, status)

    csv_filename = f"time_in_status/{status.lower().replace(' ', '_')}_{FILENAME_TIME_IN_STATUS_CSV}"
    chart_filename = f"time_in_status/{status.lower().replace(' ', '_')}_{FILENAME_TIME_IN_STATUS_CHART}"

    # output initial data
    status_df.to_csv(f"{OUTPUT_JIRA_ANALYSIS_FOLDER}{csv_filename}", index=False)

    #visualize
    visualize(status_df, f"{OUTPUT_JIRA_ANALYSIS_FOLDER}{chart_filename}", False)

