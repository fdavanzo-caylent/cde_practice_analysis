import pandas as pd
from caylent.jira.issue_throughput.analyzer import analyze
from caylent.jira.issue_throughput.visualizer import visualize
from config.config import OUTPUT_JIRA_ANALYSIS_FOLDER, FILENAME_THROUGHPUT_CSV, FILENAME_THROUGHPUT_CHART

# Configure logging
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Throughput Analysis
# Throughput measures the number of issues completed within a specific period (e.g., per sprint, per month).
def generate(issues_df):
    # generate the dataframe with analysis
    throughput_df = analyze(issues_df)

    # output initial data
    throughput_df.to_csv(f"{OUTPUT_JIRA_ANALYSIS_FOLDER}{FILENAME_THROUGHPUT_CSV}", index=False)

    #visualize
    visualize(throughput_df, f"{OUTPUT_JIRA_ANALYSIS_FOLDER}{FILENAME_THROUGHPUT_CHART}", False)

