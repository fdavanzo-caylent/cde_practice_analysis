import pandas as pd

from .utils import get_map_accounts
from config.config import MAP_MIGRATE, MAP_MOBILIZE, FILENAME_MAP_MOB_AND_MIG_ENGAGEMENTS
from .table import generate_table

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def process_map_mobilize_and_migrate_accounts(active_accounts_df, output_path, show_plot=True):
    map_mobilize_df = get_map_accounts(active_accounts_df, MAP_MOBILIZE)
    map_migrate_df = get_map_accounts(active_accounts_df, MAP_MIGRATE)
    map_df = pd.concat([map_mobilize_df, map_migrate_df])
    map_df['account'] = map_df['account'].str.slice(start=0, stop=25)

    try:
        # Number of accounts per column
        num_columns = 3

        # Initialize an empty list to store the reshaped data
        reshaped_data = []

        # Iterate over the DataFrame in steps of num_accounts_per_column
        for i in range(0, len(map_df), num_columns):
            # Select a slice of 'account' column with up to num_accounts_per_column accounts
            slice_df = map_df['account'][i:i + num_columns]
            
            # Reset the index of the slice to start from 0
            slice_df_reset = slice_df.reset_index(drop=True)
            slice_df_reset.fillna("", inplace = True) 
            
            # Append the processed slice to the reshaped_data list
            reshaped_data.append(slice_df_reset)
        
        # Create a DataFrame from the reshaped_data list and replace nulls
        reshaped_df = pd.DataFrame(reshaped_data)
        reshaped_df.fillna("", inplace = True)
    except Exception as e:
        logging.error("Error slicing the data frame into chunks: %s", e)
        raise

    # Create cell values for the table
    cell_values = [reshaped_df[col] for col in reshaped_df.columns]

    design = dict(
        layout= dict(
            width = 425,
            height = 400,
            include_header = False,
            margin={'t':10,'l':10,'b':0,'r':10}
        ),
        cells = dict(
            font_size = 8,
            align = 'left',
            font_color = 'rgb(67, 67, 67)',
            fill_color = 'rgb(212,212,212)',
            height = 22,
            width = 150
        ),
        headers = None,
    )

    generate_table(cell_values, design, output_path + FILENAME_MAP_MOB_AND_MIG_ENGAGEMENTS, show_plot)