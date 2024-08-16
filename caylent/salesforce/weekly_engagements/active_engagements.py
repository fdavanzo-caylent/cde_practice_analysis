import pandas as pd
import logging
from config.config import FILENAME_ACTIVE_ENGAGEMENTS, FILENAME_ACTIVE_ENGAGEMENTS_SUBTYPES
from .table import generate_table
from .donut import generate_donut

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def process_active_engagements(active_accounts_df, output_path, show_plot):
    try:
        # Number of accounts per column
        num_columns = 3

        # Initialize an empty list to store the reshaped data
        reshaped_data = []

        # Iterate over the DataFrame in steps of num_accounts_per_column
        for i in range(0, len(active_accounts_df), num_columns):
            # Select a slice of 'account' column with up to num_accounts_per_column accounts
            slice_df = active_accounts_df['account'][i:i + num_columns]
            
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
    # logging.debug("Cell values for the table:", cell_values)

    design = dict(
        layout= dict(
            width = 900,
            height = 500,
            include_header = False,
            margin={'t':10,'l':10,'b':10,'r':10}
        ),
        cells = dict(
            font_size = 12,
            align = 'left',
            font_color = 'rgba(40, 40, 40, 40)',
            fill_color = 'rgba(212, 212, 212, 212)',
            height = 24
        ),
        headers = None
    )

    generate_table(cell_values, design, output_path + FILENAME_ACTIVE_ENGAGEMENTS, show_plot)

def process_active_engagements_subtypes(active_accounts_df, output_path, show_plot):
    # Extract and count project subtypes
    subtype_counts = {}

    for _, row in active_accounts_df.iterrows():
        for project in row['projects']:
            subtype = project.get('subPractice')
            if subtype:
                subtype_counts[subtype] = subtype_counts.get(subtype, 0) + 1

    # Prepare data for Plotly
    labels = list(subtype_counts.keys())
    values = list(subtype_counts.values())

    generate_donut(labels, values, output_path + FILENAME_ACTIVE_ENGAGEMENTS_SUBTYPES, show_plot)