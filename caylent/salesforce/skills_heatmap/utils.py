import pandas as pd

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

HEADER_MAPPING = {
    'Contact.Full_Name__c': 'Full Name',
    'FK_pse__Skill__c.pse__Unique_Name__c': 'Skill',
    'FK_pse__Skill__c.pse__Group__c': 'Skill Group',
    'pse__Skill_Certification_Rating__c.pse__Rating__c': 'Rating'
}

def filter_core_skills(df, core_skills_path):
    try:
        core_skills_df = pd.read_csv(core_skills_path, encoding='ISO-8859-1')
        logging.debug("Core skills DataFrame columns: %s", core_skills_df.columns)
    except FileNotFoundError as e:
        logging.error("Core skills file not found: %s", e)
        raise
    except pd.errors.EmptyDataError as e:
        logging.error("Core skills file is empty: %s", e)
        raise
    except Exception as e:
        logging.error("Error reading core skills file: %s", e)
        raise

    try:
        core_skills = core_skills_df['Core Skill'].tolist()
        filtered_df = df[df['Skill'].isin(core_skills)]
        if filtered_df.empty:
            logging.error("No matching core skills found in the report data.")
            raise ValueError("No matching core skills found in the report data.")
        logging.debug("Filtered DataFrame created with %d rows", len(filtered_df))
        return filtered_df
    except KeyError as e:
        logging.error("Error accessing 'Core Skill' column: %s", e)
        raise

def calculate_percentages(filtered_df):
    try:
        total_engineers = filtered_df['Full Name'].nunique()
        pivot_counts = filtered_df.pivot_table(index='Rating', columns='Skill', aggfunc='size', fill_value=0)
        pivot_percentages = (pivot_counts / total_engineers) * 100
        if pivot_percentages.empty:
            logging.error("Pivot table calculation resulted in an empty DataFrame.")
            raise ValueError("Pivot table calculation resulted in an empty DataFrame.")
        logging.debug("Pivot table created successfully")
        return pivot_percentages
    except KeyError as e:
        logging.error("Error calculating percentages: %s", e)
        raise