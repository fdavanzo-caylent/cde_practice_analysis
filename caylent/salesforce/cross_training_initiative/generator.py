from caylent.common.salesforce_integration import query_all_salesforce
from .utils import get_skill_mappings, meets_minimum_rating
from config.config import FILENAME_CROSS_TRAINING_CSV, SKILL_WEIGHTS_MAPPING
from .visualizer import visualize, visualize_table
import logging
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def generate(sf, output_path, mappings_path, show_plot=False):
    report_data = None
    try:
        tmp_ratings_file = 'data/BI_POC.csv'
        # df = pd.read_csv(FILENAME_CROSS_TRAINING_CSV)
        df = pd.read_csv(tmp_ratings_file)
        df.columns = ['Rating-String','Rating-Nbr','Skill Group','Skill','Full Name']
        df['Rating-Nbr'] = df['Rating-Nbr'].fillna(0)
        df['Rating-String'] = df['Rating-String'].fillna('0 - No Experience')

        mapping_df = get_skill_mappings(mappings_path, 'Skill Name')
        # mapping_df = mapping_df.drop(columns=['thoughts?','Israel - Include','Danilo - Include','Raj - Include','Jorge - Include','Brian - Include'])
        mapping_df['Minimum Rating for Pillar'] = mapping_df['Minimum Rating for Pillar'].fillna(0)

        merged_df = df.merge(mapping_df, left_on='Skill', right_index=True)
        
        # Apply the function to flag rows where the required skill rating is not met
        merged_df['Meets_Required_Rating_For_Skill'] = merged_df.apply(meets_minimum_rating, axis=1)

        # Add a new column for the weight based on the skill
        merged_df['Weight'] = merged_df['Skill Weight'].map(SKILL_WEIGHTS_MAPPING)

        # Calculate the weighted rating (Rating-Nbr * Weight)
        merged_df['Weighted Rating'] = merged_df['Rating-Nbr'] * merged_df['Weight']

        # Now, aggregate the weighted ratings by Full Name and Pillar to get a readiness score
        pillar_readiness = merged_df.groupby(['Full Name', 'Pillar'])['Weighted Rating'].sum().reset_index()

        # Sort by the highest readiness score for cross-training prioritization
        pillar_readiness_sorted = pillar_readiness.sort_values(by='Weighted Rating', ascending=False)

        # Filter data to include only rows where the required skills are met
        # filtered_data = merged_df[merged_df['Meets_Required_Rating_For_Skill']]
        
        # BI_filtered_data = merged_df[merged_df['Pillar'] == 'BI & Analytics']

        # Group by 'Full Name' and 'Pillar', and calculate if they meet all minimum requirements
        grouped_data = merged_df.groupby(['Full Name', 'Pillar']).agg({
            'Weighted Rating': 'sum',  # Sum the weighted ratings
            'Meets_Required_Rating_For_Skill': 'all'  # Check if all required skills are met
        }).reset_index()

        # Sort by 'Full Name'
        grouped_data_sorted = grouped_data.sort_values(by=['Weighted Rating'], ascending=[False])

        bi_team = grouped_data_sorted[grouped_data_sorted['Meets_Required_Rating_For_Skill'] == True]
        bi_team.to_csv('output/cross_training_initiative/test_bi_team.csv')
        visualize_table(bi_team, 'output/cross_training_initiative/bi_candidates.png', 'All Team Members That Meet BI Requirements for Staffing', False)



        non_bi_team = grouped_data_sorted[grouped_data_sorted['Meets_Required_Rating_For_Skill'] == False]
        non_bi_team_names_list = non_bi_team['Full Name'].to_list()
        non_bi_team_skills = merged_df[merged_df['Full Name'].isin(non_bi_team_names_list)]
        non_bi_team_skills_reduced = non_bi_team_skills[non_bi_team_skills['Minimum Rating for Pillar'] >= 1]
        non_bi_team_skills_reduced = non_bi_team_skills[non_bi_team_skills['Meets_Required_Rating_For_Skill'] == False]
        non_bi_team_skills_reduced = non_bi_team_skills_reduced[['Full Name', 'Pillar', 'Skill', 'Rating-Nbr', 'Minimum Rating for Pillar']]
        non_bi_team_skills_sorted = non_bi_team_skills_reduced.sort_values(by=['Full Name'], ascending=[True])
        non_bi_team_skills_sorted.to_csv('output/cross_training_initiative/test_non_bi_team.csv')
        visualize_table(non_bi_team_skills_sorted, 'output/cross_training_initiative/non_bi_candidates.png', 'All Team Members That Do Not Meet BI Requirements for Staffing', False)


        ### Get best candidates for learning: ###

        ## Logic: 
        # * only one skill not meeting minimum requirement
        # * not rated 0 in skill

        # Step 1: Group by 'Full Name' and count the occurrences
        name_counts = non_bi_team_skills_sorted['Full Name'].value_counts()

        # Step 2: Filter for Full Names that occur only once
        single_occurrence_names = name_counts[name_counts == 1].index

        # Step 3: Filter the original DataFrame to include only rows where 'Full Name' occurs once
        single_occurrence_data = non_bi_team_skills_sorted[non_bi_team_skills_sorted['Full Name'].isin(single_occurrence_names)]

        # Step 3: Filter the single-occurrences to include only rows where the skill rating is >= 1
        final_learning_candidates = single_occurrence_data[single_occurrence_data['Minimum Rating for Pillar'] - single_occurrence_data['Rating-Nbr'] == 1]

        visualize_table(final_learning_candidates, 'output/cross_training_initiative/non_bi_best_candidates.png', 'Best Candidates for Next Step on BI & Analytics Training', False)


        ### END Get best candidates for learning ###

        # Display the final result
        # print(grouped_data_sorted[grouped_data_sorted['Meets_Required_Rating_For_Skill'] == True])

        # print(len(grouped_data_sorted[grouped_data_sorted['Meets_Required_Rating_For_Skill'] == True]))
        # print(pillar_readiness_sorted.head())
        # visualize(pillar_readiness_sorted)


        ####### TODO: Right now it is looking at each individual skill in the pillar and as long as they meet the minimum rating of one of the required skills, it is considering them ready
        ##### now need to take the output (don't filter out when they don't meet the minimum, maybe filter out any non-required skills then identify whether any of the skills remaining is False for meets requirement)



        # ### IDENTIFYING SINGLE-PILLAR INDIVIDUALS ###

        # # Group by 'Full Name' and count the number of unique pillars for each individual
        # single_pillar_individuals = merged_df.groupby('Full Name')['Pillar'].nunique()

        # # Filter for individuals who only have skills in one pillar
        # single_pillar_individuals = single_pillar_individuals[single_pillar_individuals == 1]

        # # Get their data
        # single_pillar_data = merged_df[merged_df['Full Name'].isin(single_pillar_individuals.index)]


        # ### ASSESSING CROSS-PILLAR SKILLS ###

        # # Filter rows where cross-training is included
        # cross_training_data = merged_df[merged_df['Include In Cross Training'] == 'Yes']

        # # Identify those with ratings of 2 or higher (some familiarity and above)
        # cross_pillar_ready = cross_training_data[cross_training_data['Rating-Nbr'] >= 2]

        # # Group by 'Full Name' to see individuals with multiple pillar readiness
        # cross_pillar_candidates = cross_pillar_ready.groupby('Full Name')['Pillar'].nunique()

        # # Identify individuals who are ready for cross-pillar training
        # cross_pillar_ready_data = cross_pillar_ready[cross_pillar_ready['Full Name'].isin(cross_pillar_candidates.index)]


        # ### SKILL GAPS AND CLIENT-READINESS ###

        # # Identify client-ready candidates (rating 3 or higher across multiple pillars)
        # client_ready_candidates = cross_pillar_ready[cross_pillar_ready['Rating-Nbr'] >= 3]

        # # Identify skill gap candidates (rating below 3)
        # skill_gap_candidates = cross_pillar_ready[cross_pillar_ready['Rating-Nbr'] < 3]

        # # Display client-ready and skill-gap candidates
        # client_ready_data = client_ready_candidates[['Full Name', 'Pillar', 'Skill', 'Rating-String']]
        # skill_gap_data = skill_gap_candidates[['Full Name', 'Pillar', 'Skill', 'Rating-String']]


        # # Export the client-ready and skill-gap candidates for review
        # cross_pillar_ready_data.sort_values(by=['Full Name', 'Pillar', 'Skill']).to_csv(f"{output_path}cross_pillar_individuals.csv", index=False)
        # single_pillar_data.sort_values(by=['Full Name', 'Pillar', 'Skill']).to_csv(f"{output_path}single_pillar_individuals.csv", index=False)
        # client_ready_data.sort_values(by=['Full Name', 'Pillar', 'Skill']).to_csv(f"{output_path}client_ready_candidates.csv", index=False)
        # skill_gap_data.sort_values(by=['Full Name', 'Pillar', 'Skill']).to_csv(f"{output_path}skill_gap_candidates.csv", index=False)


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
