from .utils import calculate_percentages, filter_core_skills, HEADER_MAPPING
from caylent.common.salesforce_integration import fetch_salesforce_report, report_to_dataframe
from config.config import HEATMAP_SKILLS_REPORT_ID, FILENAME_CORE_SKILLS
from .heatmap import generate_heatmap
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def generate(sf, core_skills_path, output_path, show_plot=False):
    
    # Fetch the Salesforce report
    report_data = fetch_salesforce_report(sf, HEATMAP_SKILLS_REPORT_ID)
    logging.info("Salesforce report fetched successfully")

    # Convert the report data to a DataFrame
    df = report_to_dataframe(report_data, HEADER_MAPPING)

    # Filter the DataFrame to include only core skills
    filtered_df = filter_core_skills(df, core_skills_path)

     # Calculate the percentages
    pivot_percentages = calculate_percentages(filtered_df)

    generate_heatmap(pivot_percentages, show_plot, output_path + FILENAME_CORE_SKILLS)

