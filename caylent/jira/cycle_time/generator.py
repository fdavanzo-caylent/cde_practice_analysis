import pandas as pd
from caylent.jira.cycle_time.analyzer import analyze
from caylent.jira.cycle_time.visualizer import visualize
from config.config import OUTPUT_JIRA_ANALYSIS_FOLDER, FILENAME_CYCLE_TIME_CSV, FILENAME_CYCLE_TIME_CHART

# Configure logging
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Cycle Time Analysis
# Cycle time is the total time it takes for an issue to go from creation to completion. This can help identify bottlenecks and inefficiencies.
def generate(issues_df):
    # generate the dataframe with analysis
    cycle_df = analyze(issues_df)

    # output initial data
    cycle_df.to_csv(f"{OUTPUT_JIRA_ANALYSIS_FOLDER}{FILENAME_CYCLE_TIME_CSV}", index=False)

    #visualize
    visualize(cycle_df, f"{OUTPUT_JIRA_ANALYSIS_FOLDER}{FILENAME_CYCLE_TIME_CHART}", False)

