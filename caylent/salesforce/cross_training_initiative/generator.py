from caylent.common.salesforce_integration import query_all_salesforce
from .utils import get_skill_mappings
from config.config import FILENAME_CROSS_TRAINING_CSV
import logging
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def generate(sf, output_path, mappings_path, show_plot=False):
    report_data = None
    try:
        df = pd.read_csv(f"{output_path}{FILENAME_CROSS_TRAINING_CSV}")
        print(df)

        print(get_skill_mappings(mappings_path))
        # query = """
        #     SELECT
        #         pse__Skill_Certification__r.pse__Group__c,
        #         pse__Skill_Certification__r.pse__Unique_Name__c,
        #         pse__Resource__r.Full_Name__c,
        #         pse__Rating__c,
        #         pse__Numerical_Rating__c
        #     FROM
        #         pse__Skill_Certification_Rating__c
        #     WHERE
        #         pse__Resource__r.pse__Practice__c = 'aFgTP0000001N110AE' 
        #         AND pse__Skill_Certification__r.pse__Group__c IN ('Data', 'GenAI')
        # """
        # cleaned_query = ' '.join(query.split())
        
        # # Fetch the Salesforce data
        # report_data = query_all_salesforce(sf, cleaned_query)
        # logging.info("Salesforce report fetched successfully")

        # df = pd.DataFrame(report_data['records']).drop('attributes', axis=1)
        # listColumns = list(df.columns)
        # for col in listColumns:
        #     if any (isinstance (df[col].values[i], dict) for i in range(0, len(df[col].values))):
        #         df = pd.concat([df.drop(columns=[col]),df[col].apply(pd.Series,dtype=df[col].dtype).drop('attributes',axis=1).add_prefix(col+'.')],axis=1)
        #         new_columns = np.setdiff1d(df.columns, listColumns)
        #         for i in new_columns:
        #             listColumns.append(i)

        # df.to_csv(f"{output_path}{FILENAME_CROSS_TRAINING_CSV}", index=False)

    except Exception as e:
        logging.error("Error processing cross training initiative data: %s", e)
        raise
