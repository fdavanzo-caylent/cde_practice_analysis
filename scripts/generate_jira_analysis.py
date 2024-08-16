import argparse
from config.config import JIRA_API_TOKEN, JIRA_USERNAME, JIRA_BASE_URL, JIRA_API_ENDPOINT, OUTPUT_JIRA_ANALYSIS_FOLDER, STATUS, FILENAME_JIRA_ISSUES_CSV
from caylent.common.jira_integration import fetch_issues, extract_issue_details
from caylent.common import generator_factory
from caylent.jira.utils import process_closed_dates

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main(username, security_token, base_url, api_endpoint, output_path):

    # get Jira data
    jql_query = "project = TDP" #TDP"#TCTDOC" EADSP, SDQP, BGOP
    issues = fetch_issues(username, security_token, base_url, api_endpoint, jql_query)
    
    # extract relevant data from jira issues
    issues_df = extract_issue_details(issues)

    # manage issues where there might be multiple closures and closed statuses
    # TODO: need to re-review what the intent here was
    issues_df = process_closed_dates(issues_df)

    # save processed jira data
    issues_df.to_csv(f"{output_path}{FILENAME_JIRA_ISSUES_CSV}", index=False)

    # Generate analysis
    generator_factory.getGenerator('WIP_ANALYSIS').generate(issues_df)
    generator_factory.getGenerator('TIME_IN_STATUS_ANALYSIS').generate(issues_df, STATUS['BLOCKED'])
    # generator_factory.getGenerator('CYCLE_TIME').generate(issues_df)
    # generator_factory.getGenerator('ISSUE_THROUGHPUT').generate(issues_df)
    # generator_factory.getGenerator('CUMULATIVE_FLOW').generate(issues_df)
    # generator_factory.getGenerator('ISSUE_STRUCTURE').generate(issues_df)
        
    logging.info("Jira analysis complete. Check the output/jira_analysis directory for results.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a heat map from Salesforce report data.')
    parser.add_argument('--username', type=str, default=JIRA_USERNAME, help='Jira username')
    parser.add_argument('--security_token', type=str, default=JIRA_API_TOKEN, help='Jira security token')
    parser.add_argument('--base_url', type=str, default=JIRA_BASE_URL, help='Base Jira URL')
    parser.add_argument('--api_endpoint', type=str, default=JIRA_API_ENDPOINT, help='Jira API endpoint')
    parser.add_argument('--output_path', type=str, default=OUTPUT_JIRA_ANALYSIS_FOLDER, help='Output folder path')

    args = parser.parse_args()

    main(args.username, args.security_token, args.base_url, args.api_endpoint, args.output_path)