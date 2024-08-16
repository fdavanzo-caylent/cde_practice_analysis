import plotly.graph_objects as go

from .utils import get_map_accounts
from config.config import MAP_ASSESS, FILENAME_MAP_ASSESS_ENGAGEMENTS
from .table import generate_table

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def process_map_assess_accounts(active_accounts_df, output_path, show_plot):
    map_assess_df = get_map_accounts(active_accounts_df, MAP_ASSESS)
    map_assess_accounts_df = map_assess_df.drop('projects', axis=1)
    # map_assess_df = get_map_accounts(active_accounts_df)
    # map_assess_df = map_assess_df.T
    map_assess_accounts_df = map_assess_accounts_df.T

    design = dict(
        layout= dict(
            width = 400,
            height = 600,
            include_header = False,
            margin={'t':10,'l':10,'b':10,'r':10}
        ),
        cells = dict(
            font_size = 18,
            align = 'left',
            font_color = 'rgb(67, 67, 67)',
            fill_color = 'rgb(212,212,212)',
            height = 30
        ),
        headers = None,
    )

    generate_table(map_assess_accounts_df, design, output_path + FILENAME_MAP_ASSESS_ENGAGEMENTS, show_plot)