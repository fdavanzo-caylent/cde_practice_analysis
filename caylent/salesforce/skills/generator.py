from .utils import get_core_skills_list, organize_skill_counts_by_category, generate_skills_percentages
from caylent.common.salesforce_integration import fetch_salesforce_report
from config.config import HEATMAP_SKILLS_REPORT_ID, FILENAME_CORE_SKILLS, FILENAME_SKILLS_COUNT, SKILLS_COUNTS_REPORT_ID, TEAM_MEMBER_REPORT_ID
from .heatmap import generate_heatmap
from .bar import generate_barchart
import logging
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def generate(sf, core_skills_path, output_path, show_plot=False):
    report_data = None
    try:
        # Fetch the team member list for calculating percentages
        team_member_report = fetch_salesforce_report(sf, TEAM_MEMBER_REPORT_ID, True)
        logging.info("Salesforce report for Team List fetched successfully")

        team_count = team_member_report['factMap']['T!T']['aggregates'][0]['value']

        # Fetch the Salesforce report
        report_data = fetch_salesforce_report(sf, HEATMAP_SKILLS_REPORT_ID, False)
        logging.info("Salesforce report fetched successfully")

        # Get our list of core skills to filter by
        core_skills = get_core_skills_list(core_skills_path)

        map_of_values = report_data['factMap']
        groupings_by_skill = report_data['groupingsDown']['groupings']
        skills = generate_skills_percentages(map_of_values, groupings_by_skill, team_count, core_skills)

        skills_df = pd.DataFrame(skills)
        skills_df.set_index('skill', inplace=True)
        skills_df = skills_df.transpose()

        generate_heatmap(skills_df, show_plot, output_path + FILENAME_CORE_SKILLS)
    except Exception as e:
        logging.error("Error processing skills heatmap: %s", e)
        raise
    
    try:
        # Fetch the Salesforce report
        report_data = fetch_salesforce_report(sf, SKILLS_COUNTS_REPORT_ID, False)
        logging.info("Salesforce report fetched successfully")

        # a lot of this is not needed atm, we don't need to combine names with numbers of skills
        # will keep the logic here for now 
        # team = get_team_members_from_grouping(report_data['groupingsDown']['groupings'])
        
        skill_counts = organize_skill_counts_by_category(report_data['factMap'])

        generate_barchart({
            '0': skill_counts['count_0_skills'],
            '1-10': skill_counts['count_1_to_10_skills'],
            '11-20': skill_counts['count_11_to_20_skills'],
            '20+': skill_counts['count_20_plus_skills']
        }, show_plot, output_path + FILENAME_SKILLS_COUNT)

    except Exception as e:
        logging.error("Error processing active engagements: %s", e)
        raise
