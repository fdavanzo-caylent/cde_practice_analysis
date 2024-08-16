import pandas as pd
from config.config import MAP_MIGRATE, MAP_MOBILIZE, MAP_ASSESS

ACTIVE_ENGAGEMENTS_HEADER_MAPPING = {
    'FK_pse__Proj__c.pse__Account__c': 'account',
    'FK_NAME': 'project',
    'pse__Assignment__c.pse__Role__c': 'role',
    'pse__Assignment__c.pse__Resource__c': 'name',
    'FK_pse__Proj__c.pse__Start_Date__c': 'start',
    'FK_pse__Proj__c.pse__End_Date__c': 'end',
    'FK_pse__Proj__c.pse__Practice__c': 'practice',
    'FK_pse__Proj__c.Sub_Practice__c': 'sub_practice',
    'FK_pse__Proj__c.Delivery_Type__c': 'delivery_type',
    'FK_pse__Proj__c.AWS_MAP_Phase__c': 'map_phases'
}

FUTURE_ENGAGEMENTS_HEADER_MAPPING = {
    'pse__Proj__c.pse__Account__c.Name': 'account',
    'pse__Proj__c.Name': 'project',
    'pse__Resource_Request__c.pse__Resource_Role__c': 'role',
    'pse__Resource_Request__c.pse__Staffer_Resource__c.Name': 'name',
    'pse__Resource_Request__c.pse__Start_Date__c': 'start',
    'pse__Resource_Request__c.pse__End_Date__c': 'end',
    'pse__Proj__c.pse__Practice__c.Name': 'practice',
    'pse__Proj__c.Sub_Practice__c': 'sub_practice',
    'pse__Proj__c.Delivery_Type__c': 'delivery_type',
    'pse__Proj__c.AWS_MAP_Phase__c': 'map_phases'
}

MAP_PHASE = {
    'MAP_ASSESS': 'Assess',
    'MAP_MOBILIZE': 'Mobilize',
    'MAP_MIGRATE': 'Migrate'
}

def aggregate_report_data(df):
    result = []

    # Helper function to find if account already exists in the result
    def find_account(account_name):
        for account in result:
            if account['account'] == account_name:
                return account
        return None

    # Helper function to find if a project already exists under an account
    def find_project(account, project_name):
        for project in account['projects']:
            if project['project'] == project_name:
                return project
        return None

    # Iterate over each row in the DataFrame
    for _, item in df.iterrows():
        account_entry = find_account(item['account'])
        if not account_entry:
            # Create a new account entry if not found
            account_entry = {'account': item['account'], 'projects': []}
            result.append(account_entry)

        project_entry = find_project(account_entry, item['project'])
        if not project_entry:
            # Create a new project entry if not found
            map_phases = item['map_phases'].split(';')

            project_entry = {
                'project': item['project'],
                'startDate': item['start'],
                'endDate': item['end'],
                'primaryPractice': item['practice'],
                'subPractice': item['sub_practice'],
                'deliveryType': item['delivery_type'],
                'isMapAssess': MAP_ASSESS in map_phases,
                'isMapMigrate': MAP_MIGRATE in map_phases,
                'isMapMobilize': MAP_MOBILIZE in map_phases,
                'roles': [],
                'team': []
            }
            account_entry['projects'].append(project_entry)

        project_entry['roles'].append(item['role'])
        project_entry['team'].append(item['name'])

    return pd.DataFrame(result)

def get_map_accounts(accounts_df, phase):
    map_accounts = []

    # Iterate over each row in the DataFrame
    for index, row in accounts_df.iterrows():
        projects = row['projects']
        map_projects = []

        for project in projects:
            # Check if the project matches the given map phase
            if phase and project.get("isMap" + phase):
                map_projects.append(project)

        if map_projects:
            map_accounts.append({
                'account': row['account'],
                'projects': map_projects
            })

    return pd.DataFrame(map_accounts)

# def get_map_accounts(accounts_df):
#     map_accounts = []

#     # Iterate over each row in the DataFrame
#     for index, row in accounts_df.iterrows():
#         projects = row['projects']
#         map_phases = []

#         for project in projects:
#             # Check if the project matches the given map phase
#             if project.get('isMapAssess'):
#                 map_phases.append('Assess')
#             if project.get('isMapMobilize'):
#                 map_phases.append('Mobilize')
#             if project.get('isMapMigrate'):
#                 map_phases.append('Migrate')

#         if len(map_phases) > 0:
#             map_accounts.append({
#                 'account': row['account'],
#                 'phases': map_phases
#             })

#     return pd.DataFrame(map_accounts)