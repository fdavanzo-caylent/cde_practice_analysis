import pandas as pd
from caylent.jira.cumulative_flow.analyzer import analyze
from caylent.jira.cumulative_flow.visualizer import visualize
from config.config import OUTPUT_JIRA_ANALYSIS_FOLDER, FILENAME_CUMULATIVE_FLOW_CSV, FILENAME_CUMULATIVE_FLOW_CHART

# Configure logging
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Cumulative Flow Diagram
# A Cumulative Flow Diagram (CFD) helps visualize the flow of issues through different statuses over time, highlighting bottlenecks and flow distribution.
def generate(issues_df):
    # generate the dataframe with analysis
    cf_df = analyze(issues_df)

    # output initial data
    cf_df.to_csv(f"{OUTPUT_JIRA_ANALYSIS_FOLDER}{FILENAME_CUMULATIVE_FLOW_CSV}", index=False)

    #visualize
    visualize(cf_df, f"{OUTPUT_JIRA_ANALYSIS_FOLDER}{FILENAME_CUMULATIVE_FLOW_CHART}", False)

