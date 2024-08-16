import pandas as pd
from caylent.jira.work_in_progress.analyzer import analyze
from caylent.jira.work_in_progress.visualizer import visualize_line_chart, visualize_bar_chart
from config.config import OUTPUT_JIRA_ANALYSIS_FOLDER, FILENAME_WIP_ANALYSIS_CSV, FILENAME_WIP_ANALYSIS_CHART, FILENAME_WIP_ANALYSIS_BAR_CHART

# Configure logging
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Work in Progress (WIP) Analysis
# WIP analysis helps understand the number of issues being worked on at any given time, aiding in managing team workload and identifying over-commitment.
def generate(issues_df):
    # generate the dataframe with analysis
    wip_data = analyze(issues_df)

    # add in a proper datetime so any future charting will not show dates from the 1960s
    wip_data['status_change_date'] = pd.to_datetime(wip_data['status_change_date'], format='%Y-%m-%d')

    # output initial data
    wip_data.to_csv(f"{OUTPUT_JIRA_ANALYSIS_FOLDER}{FILENAME_WIP_ANALYSIS_CSV}", index=False)

    #visualize
    visualize_line_chart(wip_data, OUTPUT_JIRA_ANALYSIS_FOLDER + FILENAME_WIP_ANALYSIS_CHART, False)
    visualize_bar_chart(wip_data, OUTPUT_JIRA_ANALYSIS_FOLDER + FILENAME_WIP_ANALYSIS_BAR_CHART, False)

