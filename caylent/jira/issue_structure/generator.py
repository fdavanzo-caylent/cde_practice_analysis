import pandas as pd
from caylent.jira.issue_structure.analyzer import analyze
from caylent.jira.issue_structure.visualizer import visualize
from config.config import OUTPUT_JIRA_ANALYSIS_FOLDER, FILENAME_ISSUE_STRUCTURE_CSV, FILENAME_ISSUE_STRUCTURE_CHART

# Configure logging
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def generate(issues_df):
    # generate the dataframe with analysis
    status_df = analyze(issues_df)

    # output initial data
    status_df.to_csv(f"{OUTPUT_JIRA_ANALYSIS_FOLDER}{FILENAME_ISSUE_STRUCTURE_CSV}", index=False)

    #visualize
    visualize(status_df, f"{OUTPUT_JIRA_ANALYSIS_FOLDER}{FILENAME_ISSUE_STRUCTURE_CHART}", False)

