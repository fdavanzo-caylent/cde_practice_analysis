from simple_salesforce import Salesforce
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def authenticate_salesforce(username, password, security_token):
    try:
        return Salesforce(username=username, password=password, security_token=security_token)
    except Exception as e:
        logging.error("Error authenticating with Salesforce: %s", e)
        raise

def fetch_salesforce_report(sf, report_id):
    try:
        report = sf.restful('analytics/reports/{}'.format(report_id))
        return report
    except Exception as e:
        logging.error("Error fetching Salesforce report: %s", e)
        raise

def report_to_dataframe(report_data, header_replacement_map):
    try:
        # logging.debug(f"Detail Columns: {report_data['reportMetadata']['detailColumns']}")
        sf_columns = report_data['reportMetadata']['detailColumns']
        mapped_columns = list(map(lambda item: header_replacement_map.get(item, item), sf_columns))
    except KeyError as e:
        logging.error("Error accessing 'reportMetadata' or 'detailColumns': %s", e)
        raise

    try:
        rows = [
            [cell.get('label', '') for cell in row['dataCells']]
            for row in report_data['factMap']['T!T']['rows']
        ]
    except KeyError as e:
        logging.error("Error accessing 'factMap' or 'T!T' or 'rows': %s", e)
        raise

    df = pd.DataFrame(rows, columns=mapped_columns)
    # logging.debug("DataFrame created successfully with columns: %s", df.columns)
    return df