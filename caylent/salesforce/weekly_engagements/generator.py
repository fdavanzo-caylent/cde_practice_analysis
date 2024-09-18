from .utils import ACTIVE_ENGAGEMENTS_HEADER_MAPPING, FUTURE_ENGAGEMENTS_HEADER_MAPPING, aggregate_report_data
from .active_engagements import process_active_engagements, process_active_engagements_subtypes
from .active_map_assess import process_map_assess_accounts
from .active_map_mobilize_and_migrate import process_map_mobilize_and_migrate_accounts
from .future_engagements import process_future_engagements, process_future_engagements_subtypes
from .future_map import process_future_map
from caylent.common.salesforce_integration import fetch_salesforce_report, report_to_dataframe
from config.config import ACTIVE_ENGAGEMENTS_REPORT_ID, FUTURE_ENGAGEMENTS_REPORT_ID

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def generate(sf, output_path, show_plot=True):

    # Active Engagements
    try:
        # Fetch the Salesforce report
        active_engagements_report_data = fetch_salesforce_report(sf, ACTIVE_ENGAGEMENTS_REPORT_ID, True)
        logging.info("Salesforce report fetched successfully")

        # Convert the report data to a DataFrame
        active_engagements_df = report_to_dataframe(active_engagements_report_data, ACTIVE_ENGAGEMENTS_HEADER_MAPPING)

        # Aggregate data by account
        active_accounts_df = aggregate_report_data(active_engagements_df)

        process_active_engagements(active_accounts_df, output_path, show_plot)
        process_active_engagements_subtypes(active_accounts_df, output_path, show_plot)
        process_map_assess_accounts(active_accounts_df, output_path, show_plot)
        process_map_mobilize_and_migrate_accounts(active_accounts_df, output_path, show_plot)

        logging.info("Completed processing of active engagements")
    except Exception as e:
        logging.error("Error processing active engagements: %s", e)
        raise

    # Future Engagements
    try:
        # Fetch the Salesforce report
        future_engagements_report_data = fetch_salesforce_report(sf, FUTURE_ENGAGEMENTS_REPORT_ID, True)
        logging.info("Salesforce report fetched successfully")

        # Convert the report data to a DataFrame
        future_engagements_df = report_to_dataframe(future_engagements_report_data, FUTURE_ENGAGEMENTS_HEADER_MAPPING)

        # Aggregate data by account
        future_accounts_df = aggregate_report_data(future_engagements_df)

        process_future_engagements(future_accounts_df, output_path, show_plot)
        process_future_engagements_subtypes(future_accounts_df, output_path, show_plot)
        process_future_map(future_accounts_df, output_path, show_plot)

        logging.info("Completed processing of future engagements")
    except Exception as e:
        logging.error("Error processing future engagements: %s", e)
        raise
