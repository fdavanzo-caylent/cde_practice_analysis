import pandas as pd

# Configure logging
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def analyze(issues_df):
    results = []
    for _, row in issues_df.iterrows():
        user_story_format = check_user_story_format(row['description']) if row['issue_type'] == 'Story' else None
        missing_fields = []

        if row['issue_type'] == 'Story' and not user_story_format:
            missing_fields.append("User Story Format")
        if row['issue_type'] in ['Story', 'Task'] and not row['story_points']:
            missing_fields.append("Story Points")
        if not row['priority']:
            missing_fields.append("Priority")
        if not row['assignee']:
            missing_fields.append("Assignee")

        results.append({
            'issue_key': row['issue_key'],
            'issue_type': row['issue_type'],
            'missing_fields': ", ".join(missing_fields) if missing_fields else None
        })

    return pd.DataFrame(results)

def check_user_story_format(description):
    if description and "As a" in description and "I want" in description and "so that" in description:
        return True
    return False
