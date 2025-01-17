import argparse
from caylent.common.salesforce_integration import authenticate_salesforce
from caylent.common import generator_factory
from config.config import CROSS_TRAINING_MAPPING_PATH, PASSWORD, SECURITY_TOKEN, USERNAME, OUTPUT_CROSS_TRAINING_INITIATIVE_FOLDER
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main(username, password, security_token, mapping_path, output_path, show_plot=False):
    
    # Authenticate with Salesforce
    sf = authenticate_salesforce(username, password, security_token)
    logging.info("Authenticated with Salesforce successfully")


    tmp_mapping_file = 'data/Cross_Training_BI_Analytics_POC.csv'
    # generator_factory.getGenerator('CROSS_TRAINING_INITIATIVE').generate(sf, output_path, mapping_path, show_plot)
    generator_factory.getGenerator('CROSS_TRAINING_INITIATIVE').generate(sf, output_path, tmp_mapping_file, show_plot)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process cross training initiative data.')
    parser.add_argument('--username', type=str, default=USERNAME, help='Salesforce username')
    parser.add_argument('--password', type=str, default=PASSWORD, help='Salesforce password')
    parser.add_argument('--security_token', type=str, default=SECURITY_TOKEN, help='Salesforce security token')
    parser.add_argument('--mapping_path', type=str, default=CROSS_TRAINING_MAPPING_PATH, help='Path to the mapping CSV file')
    parser.add_argument('--output_path', type=str, default=OUTPUT_CROSS_TRAINING_INITIATIVE_FOLDER, help='Output folder path')
    parser.add_argument('--no-show', action='store_false', help='Do not show the heatmap plot')

    args = parser.parse_args()

    main(args.username, args.password, args.security_token, args.mapping_path, args.output_path, show_plot=args.no_show)
