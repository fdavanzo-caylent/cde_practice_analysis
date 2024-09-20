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
        df.columns = ['Rating-String','Rating-Nbr','Skill Group','Skill','Full Name']

        mapping_df = get_skill_mappings(mappings_path, 'Skill Name')
        mapping_df = mapping_df.drop(columns=['thoughts?','Israel - Include','Danilo - Include','Raj - Include','Jorge - Include','Brian - Include'])

        merged_df = df.merge(mapping_df, left_on='Skill', right_index=True)

        ### IDENTIFYING SINGLE-PILLAR INDIVIDUALS ###

        # Group by 'Full Name' and count the number of unique pillars for each individual
        single_pillar_individuals = merged_df.groupby('Full Name')['Pillar'].nunique()

        # Filter for individuals who only have skills in one pillar
        single_pillar_individuals = single_pillar_individuals[single_pillar_individuals == 1]

        # Get their data
        single_pillar_data = merged_df[merged_df['Full Name'].isin(single_pillar_individuals.index)]


        ### ASSESSING CROSS-PILLAR SKILLS ###

        # Filter rows where cross-training is included
        cross_training_data = merged_df[merged_df['Include In Cross Training'] == 'Yes']

        # Identify those with ratings of 2 or higher (some familiarity and above)
        cross_pillar_ready = cross_training_data[cross_training_data['Rating-Nbr'] >= 2]

        # Group by 'Full Name' to see individuals with multiple pillar readiness
        cross_pillar_candidates = cross_pillar_ready.groupby('Full Name')['Pillar'].nunique()

        # Identify individuals who are ready for cross-pillar training
        cross_pillar_ready_data = cross_pillar_ready[cross_pillar_ready['Full Name'].isin(cross_pillar_candidates.index)]


        ### SKILL GAPS AND CLIENT-READINESS ###

        # Identify client-ready candidates (rating 3 or higher across multiple pillars)
        client_ready_candidates = cross_pillar_ready[cross_pillar_ready['Rating-Nbr'] >= 3]

        # Identify skill gap candidates (rating below 3)
        skill_gap_candidates = cross_pillar_ready[cross_pillar_ready['Rating-Nbr'] < 3]

        # Display client-ready and skill-gap candidates
        client_ready_data = client_ready_candidates[['Full Name', 'Pillar', 'Skill', 'Rating-String']]
        skill_gap_data = skill_gap_candidates[['Full Name', 'Pillar', 'Skill', 'Rating-String']]


        # Export the client-ready and skill-gap candidates for review
        cross_pillar_ready_data.sort_values(by=['Full Name', 'Pillar', 'Skill']).to_csv(f"{output_path}cross_pillar_individuals.csv", index=False)
        single_pillar_data.sort_values(by=['Full Name', 'Pillar', 'Skill']).to_csv(f"{output_path}single_pillar_individuals.csv", index=False)
        client_ready_data.sort_values(by=['Full Name', 'Pillar', 'Skill']).to_csv(f"{output_path}client_ready_candidates.csv", index=False)
        skill_gap_data.sort_values(by=['Full Name', 'Pillar', 'Skill']).to_csv(f"{output_path}skill_gap_candidates.csv", index=False)


        # merged_df['Full Name'] = '****'
        # merged_df.head(200).to_csv(f"{output_path}tmp_obfuscated.csv")




        # I wonder whether I should export the id of the skills and use that to do mappings???
        # go through the df and add the different categories/pillars to the rows of the SF data
        # should we apply weights to the different skills and or skill ratings?
        # use the weighted value to identify if the person is a good candidate to cover multiple pillars or needs to cross-train
        # also identify how many are trained in the various pillars at a high/med/low skill level


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
