import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
from common.salesforce_integration import authenticate_salesforce, fetch_salesforce_report, report_to_dataframe

class TestSalesforceIntegration(unittest.TestCase):
    
    @patch('common.salesforce_integration.Salesforce')
    def test_authenticate_salesforce(self, MockSalesforce):
        sf_instance = MagicMock()
        MockSalesforce.return_value = sf_instance
        
        username = 'test_user'
        password = 'test_password'
        security_token = 'test_token'
        
        sf = authenticate_salesforce(username, password, security_token)
        
        MockSalesforce.assert_called_with(username=username, password=password, security_token=security_token)
        self.assertEqual(sf, sf_instance)
    
    @patch('common.salesforce_integration.Salesforce')
    def test_fetch_salesforce_report(self, MockSalesforce):
        sf_instance = MagicMock()
        report_id = 'test_report_id'
        report_data = {'report': 'data'}
        sf_instance.restful.return_value = report_data
        MockSalesforce.return_value = sf_instance
        
        sf = authenticate_salesforce('test_user', 'test_password', 'test_token')
        report = fetch_salesforce_report(sf, report_id)
        
        sf.restful.assert_called_with('analytics/reports/test_report_id')
        self.assertEqual(report, report_data)

    def test_report_to_dataframe(self):
        report_data = {
            'reportMetadata': {
                'detailColumns': ['Contact.Full_Name__c', 'FK_pse__Skill__c.pse__Unique_Name__c', 'pse__Skill_Certification_Rating__c.pse__Rating__c']
            },
            'factMap': {
                'T!T': {
                    'rows': [
                        {'dataCells': [{'label': 'Engineer1'}, {'label': 'Skill1'}, {'label': '3'}]},
                        {'dataCells': [{'label': 'Engineer2'}, {'label': 'Skill2'}, {'label': '4'}]}
                    ]
                }
            }
        }
        
        df = report_to_dataframe(report_data, {
            'Contact.Full_Name__c': 'Full Name',
            'FK_pse__Skill__c.pse__Unique_Name__c': 'Skill',
            'FK_pse__Skill__c.pse__Group__c': 'Skill Group',
            'pse__Skill_Certification_Rating__c.pse__Rating__c': 'Rating'
        })

        expected_df = pd.DataFrame({
            'Full Name': ['Engineer1', 'Engineer2'],
            'Skill': ['Skill1', 'Skill2'],
            'Rating': ['3', '4']
        })
        pd.testing.assert_frame_equal(df, expected_df)

if __name__ == '__main__':
    unittest.main()