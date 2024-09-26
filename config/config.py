import os

# Salesforce credentials
USERNAME = os.getenv("SALESFORCE_UNAME")
PASSWORD = os.getenv("SALESFORCE_PWD")
SECURITY_TOKEN = os.getenv("SALESFORCE_TOKEN")

# Salesforce report ID
HEATMAP_SKILLS_REPORT_ID = '00OTP000002ESJR2A4'
ACTIVE_ENGAGEMENTS_REPORT_ID = '00OTP000001JUbJ2AW'
FUTURE_ENGAGEMENTS_REPORT_ID = '00OTP000001Q2FJ2A0'
ALL_CAYLENT_SKILLS_REPORT_ID = '00OTP000001nWWM2A2'
SKILLS_COUNTS_REPORT_ID = '00OTP000002Eozt2AC'
TEAM_MEMBER_REPORT_ID = '00OTP000002Ek6f2AC'

# Path to CSV files
CORE_SKILLS_PATH = 'data/core_skills.csv'
SKILLS_RATINGS_PATH = 'data/skills_ratings.csv'
CROSS_TRAINING_MAPPING_PATH = 'data/cross_training_mappings.csv'
FILENAME_CROSS_TRAINING_CSV = 'data/cross_training_skills.csv'

# report-specific filters
FILTER_FOR_SKILL_LEVEL_ZERO = '0 - No Rating'

# MAP Phases
MAP_ASSESS = 'Assess'
MAP_MIGRATE = 'Migrate'
MAP_MOBILIZE = 'Mobilize'

# Report Output Locations
OUTPUT_WEEKLY_STATUS_FOLDER = 'output/weekly_status/'
FILENAME_ACTIVE_ENGAGEMENTS = 'active_engagements_table.png'
FILENAME_ACTIVE_ENGAGEMENTS_SUBTYPES = 'active_engagements_subtypes.png'
FILENAME_MAP_ASSESS_ENGAGEMENTS = 'active_map_assess_engagements_table.png'
FILENAME_MAP_MOB_AND_MIG_ENGAGEMENTS = 'active_map_mob_and_mig_engagements_table.png'
FILENAME_CORE_SKILLS = 'core_skills_heatmap.png'
FILENAME_SKILLS_COUNT = 'skills_count_bar_chart.png'
FILENAME_FUTURE_ENGAGEMENTS = 'future_engagements_table.png'
FILENAME_FUTURE_MAP_ENGAGEMENTS = 'future_map_engagements_table.png'
FILENAME_FUTURE_ENGAGEMENTS_SUBTYPES = 'future_engagements_subtypes.png'
FILENAME_JIRA_ISSUES_CSV = 'all_issues.csv'
FILENAME_WIP_ANALYSIS_CSV = 'wip/wip_analysis.csv'
FILENAME_WIP_ANALYSIS_CHART = 'wip/wip_analysis.png'
FILENAME_WIP_ANALYSIS_BAR_CHART = 'wip/wip_stacked_bar_chart.png'
FILENAME_CYCLE_TIME_CSV = 'cycle_time/cycle_time_analysis.csv'
FILENAME_CYCLE_TIME_CHART = 'cycle_time/cycle_time_analysis.png'
FILENAME_THROUGHPUT_CSV = 'issue_throughput/issue_throughput_analysis.csv'
FILENAME_THROUGHPUT_CHART = 'issue_throughput/issue_throughput_analysis.png'
FILENAME_CUMULATIVE_FLOW_CSV = 'cumulative_flow/cumulative_flow_analysis.csv'
FILENAME_CUMULATIVE_FLOW_CHART = 'cumulative_flow/cumulative_flow_analysis.png'
FILENAME_ISSUE_STRUCTURE_CSV = 'issue_structure/issue_structure_analysis.csv'
FILENAME_ISSUE_STRUCTURE_CHART = 'issue_structure/issue_structure_analysis.png'
FILENAME_TIME_IN_STATUS_CSV = 'time_analysis.csv'
FILENAME_TIME_IN_STATUS_CHART = 'time_analysis_chart.png'

OUTPUT_JIRA_ANALYSIS_FOLDER = 'output/jira_analysis/'
OUTPUT_CROSS_TRAINING_INITIATIVE_FOLDER = 'output/cross_training_initiative/'

# Jira credentials
JIRA_USERNAME = os.getenv("JIRA_UNAME")
JIRA_API_TOKEN = os.getenv("JIRA_TOKEN")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_API_ENDPOINT = os.getenv("JIRA_API_ENDPOINT")

# WIP Analysis
WIP_ALL_ISSUE_STATUSES = ["In Review", "In Progress", "Blocked", "Done", "Closed"]
WIP_ISSUE_STATUSES_TO_TRACK = ["In Review", "In Progress", "Blocked"]

# STATUS Analysis
STATUS = {
    'BLOCKED': 'Blocked',
    'IN_REVIEW': 'In Review',
    'IN_PROGRESS': 'In Progress',
    'DONE': 'Done',
    'CLOSED': 'Closed'
}

# Skill Weights
SKILL_WEIGHTS_MAPPING = {
    'High Priority': 1.5,
    'Medium Priority': 1.2,
    'Low Priority': 1.0,
}