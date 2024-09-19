import pandas as pd

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_skill_mappings(mappings_path):
    try:
        mappings_df = pd.read_csv(mappings_path, encoding='ISO-8859-1')
        logging.debug("Mappings DataFrame columns: %s", mappings_df.columns)

        return mappings_df.to_dict('records')
    except FileNotFoundError as e:
        logging.error("Core skills file not found: %s", e)
        raise
    except pd.errors.EmptyDataError as e:
        logging.error("Core skills file is empty: %s", e)
        raise
    except Exception as e:
        logging.error("Error reading core skills file: %s", e)
        raise