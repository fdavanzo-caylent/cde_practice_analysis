import pandas as pd
import math
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_core_skills_list(core_skills_path):
    try:
        core_skills_df = pd.read_csv(core_skills_path, encoding='ISO-8859-1')
        logging.debug("Core skills DataFrame columns: %s", core_skills_df.columns)

        return core_skills_df['Core Skill'].tolist()
    except FileNotFoundError as e:
        logging.error("Core skills file not found: %s", e)
        raise
    except pd.errors.EmptyDataError as e:
        logging.error("Core skills file is empty: %s", e)
        raise
    except Exception as e:
        logging.error("Error reading core skills file: %s", e)
        raise

def filter_skills_with_no_rating(df, ratings_path):
    try:
        core_skills_df = pd.read_csv(ratings_path, encoding='ISO-8859-1')
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

def filter_out_skill_levels(skills_df, skills_to_filter):
    filtered_df = skills_df[~skills_df['Rating'].isin(skills_to_filter)]
    if filtered_df.empty:
        logging.error("No skill ratings found in the report data.")
        raise ValueError("No skill ratings found in the report data.")

    logging.debug("Filtered DataFrame created with %d rows", len(filtered_df))
    return filtered_df

def get_team_members_from_grouping(grouping_by_team_member):
    team = {}
    for member_record in grouping_by_team_member:
        team[member_record['key']] = {'name': member_record['value']}
    
    return team

def organize_skill_counts_by_category(fact_map):
    skill_counts = {
        'count_0_skills': 0,
        'count_1_to_10_skills': 0,
        'count_11_to_20_skills': 0,
        'count_20_plus_skills': 0,
    }

    for key in fact_map:
        if key == 'T!T': continue #skip the totals row

        skill_count = int(fact_map[key]['aggregates'][0]['value'])
        if skill_count == 0: 
            skill_counts['count_0_skills'] = skill_counts['count_0_skills'] + 1
        elif skill_count >= 1 and skill_count <= 10: 
            skill_counts['count_1_to_10_skills'] = skill_counts['count_1_to_10_skills'] + 1
        elif skill_count >= 11 and skill_count <= 20: 
            skill_counts['count_11_to_20_skills'] = skill_counts['count_11_to_20_skills'] + 1
        else: 
            skill_counts['count_20_plus_skills'] = skill_counts['count_20_plus_skills'] + 1
        
    return skill_counts

def generate_skills_percentages(map_of_values, groupings_by_skill, team_count, core_skills):
    skills = []
        
    for skill_record in groupings_by_skill:
        skill_id = skill_record['key']
        skill_value = skill_record['value']
        
        # skip if the skilll is not a core skill
        if skill_value not in core_skills: continue

        ratings = {
                '0 - No Rating': math.ceil((map_of_values[f"{skill_id}!{0}"]['aggregates'][0]['value'] / team_count) * 100),
                '1 - Limited Exposure': math.ceil((map_of_values[f"{skill_id}!{1}"]['aggregates'][0]['value'] / team_count) * 100),
                '2 - Some Familiarity': math.ceil((map_of_values[f"{skill_id}!{2}"]['aggregates'][0]['value'] / team_count) * 100),
                '3 - Comfortable': math.ceil((map_of_values[f"{skill_id}!{3}"]['aggregates'][0]['value'] / team_count) * 100),
                '4 - Strong': math.ceil((map_of_values[f"{skill_id}!{4}"]['aggregates'][0]['value'] / team_count) * 100),
                '5 - Expert': math.ceil((map_of_values[f"{skill_id}!{5}"]['aggregates'][0]['value'] / team_count) * 100)
            }
        flattened_row = {'skill': skill_value}
        flattened_row.update(ratings)
        skills.append(flattened_row)
    
    return skills