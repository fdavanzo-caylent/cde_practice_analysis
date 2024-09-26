import pandas as pd

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_skill_mappings(mappings_path, index):
    try:
        mappings_df = pd.read_csv(mappings_path, encoding='ISO-8859-1')
        logging.debug("Mappings DataFrame columns: %s", mappings_df.columns)

        # this may not make sense but keeping it here for the moment as it might make things easier to map
        mappings_df.set_index(index, inplace = True)
        # return mappings_df.to_dict('records')
        return mappings_df
    except FileNotFoundError as e:
        logging.error("Mappings file not found: %s", e)
        raise
    except pd.errors.EmptyDataError as e:
        logging.error("Mappings file is empty: %s", e)
        raise
    except Exception as e:
        logging.error("Error reading Mappings file: %s", e)
        raise

# Function to check if an individual meets the minimum rating for required skills
def meets_minimum_rating(row):
    rating = row['Rating-Nbr']
    min_rating = row['Minimum Rating for Pillar']
    
    # Check if the skill is a required skill for the pillar and if the rating is sufficient
    return rating >= min_rating
