import plotly.graph_objects as go
import pandas as pd

from .utils import get_map_accounts
from config.config import MAP_ASSESS, MAP_MIGRATE, MAP_MOBILIZE, FILENAME_FUTURE_MAP_ENGAGEMENTS
from .table import generate_table

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def process_future_map(future_accounts_df, output_path, show_plot):
    map_assess_df = get_map_accounts(future_accounts_df, MAP_ASSESS)
    map_mobilize_df = get_map_accounts(future_accounts_df, MAP_MOBILIZE)
    map_migrate_df = get_map_accounts(future_accounts_df, MAP_MIGRATE)
    map_df = pd.concat([map_assess_df, map_mobilize_df, map_migrate_df])
    map_df['account'] = map_df['account'].str.slice(start=0, stop=25)

    map_accounts_df = map_df.drop('projects', axis=1)
    map_accounts_df = map_accounts_df.T

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

    generate_table(map_accounts_df, design, output_path + FILENAME_FUTURE_MAP_ENGAGEMENTS, show_plot)