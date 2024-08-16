import logging
from config.config import FILENAME_FUTURE_ENGAGEMENTS, FILENAME_FUTURE_MAP_ENGAGEMENTS_SUBTYPES
from .table import generate_table
from .donut import generate_donut

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def process_future_engagements(future_accounts_df, output_path, show_plot):

    accounts = []
    projects = []
    start_dates = []
    end_dates = []
    delivery_types = []
    primary_practices = []
    sub_practices = []
    teams = []
    for _, row in future_accounts_df.iterrows():
        account = row['account']
        for project in row['projects']:
            accounts.append(account)
            projects.append(project['project'])
            start_dates.append(project['startDate'])
            end_dates.append(project['endDate'])
            delivery_types.append(project['deliveryType'])
            primary_practices.append(project['primaryPractice'][:3])
            sub_practices.append(project['subPractice'][:25])
            teams.append(', '.join(str(x) for x in project['team']))

    future_engagement_table_cells = [
        accounts,
        projects,
        start_dates,
        end_dates,
        delivery_types,
        primary_practices,
        sub_practices,
        teams]
    
    design = dict(
        layout= dict(
            width = 1100,
            height = 1500,
            include_header = False,
            margin={'t':10,'l':10,'b':10,'r':10},
            column_widths = [185, 250, 80, 80, 60, 60, 100, 250]
        ),
        cells = dict(
            font_size = 12,
            align = 'left',
            font_color = 'rgb(67, 67, 67)',
            fill_color = 'rgb(212,212,212)',
            height = 28
        ),
        headers = dict(
            values=['Account', 'Project', 'Start', 'End', 'Type', 'Practice', 'Sub-Practice', 'Team'],  # Set header values
            fill_color='paleturquoise',  # Set header fill color
            align='left'  # Align header text to the left
        )
    )
    generate_table(future_engagement_table_cells, design, output_path + FILENAME_FUTURE_ENGAGEMENTS, show_plot)

def process_future_engagements_subtypes(future_accounts_df, output_path, show_plot):
    # Extract and count project subtypes
    subtype_counts = {}

    for _, row in future_accounts_df.iterrows():
        for project in row['projects']:
            subtype = project.get('subPractice')
            if subtype:
                subtype_counts[subtype] = subtype_counts.get(subtype, 0) + 1

    # Prepare data for Plotly
    labels = list(subtype_counts.keys())
    values = list(subtype_counts.values())

    generate_donut(labels, values, output_path + FILENAME_FUTURE_MAP_ENGAGEMENTS_SUBTYPES, show_plot)
