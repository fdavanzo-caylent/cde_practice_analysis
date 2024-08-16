import requests
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_issues(username, security_token, base_url, api_endpoint, jql_query):
    url = base_url + api_endpoint
    headers = {
        "Accept": "application/json"
    }
    params = {
        "jql": jql_query,
        "expand": "changelog",
        "maxResults": 1000
    }

    response = requests.get(url, headers=headers, params=params, auth=(username, security_token))
    response.raise_for_status()
    issues = response.json()['issues']
    
    return issues

def extract_history(issues):
    data = []
    for issue in issues:
        issue_key = issue['key']
        for history in issue['changelog']['histories']:
            for item in history['items']:
                if item['field'] == 'status':
                    data.append({
                        'issue_key': issue_key,
                        'status_from': item['fromString'],
                        'status_to': item['toString'],
                        'status_change_date': history['created']
                    })

    return pd.DataFrame(data)

def extract_issue_details(issues):
    data = []

    for issue in issues:
        for history in issue['changelog']['histories']:
            for item in history['items']:
                if item['field'] == 'status':
                    data.append({
                        'issue_key': issue['key'],
                        'summary': issue['fields']['summary'],
                        'description': issue['fields']['description'],
                        'issue_type': issue['fields']['issuetype']['name'],
                        'created': issue['fields']['created'],
                        'updated': issue['fields']['updated'],
                        'status': issue['fields']['status']['name'],
                        'priority': issue['fields']['priority']['name'] if issue['fields']['priority'] else None,
                        'labels': issue['fields']['labels'],
                        'assignee': issue['fields']['assignee']['displayName'] if issue['fields']['assignee'] else None,
                        'reporter': issue['fields']['reporter']['displayName'],
                        'story_points': issue['fields'].get('customfield_10004'),
                        'status_from': item['fromString'],
                        'status_to': item['toString'],
                        'status_change_date': history['created']
                    })

    return pd.DataFrame(data)
