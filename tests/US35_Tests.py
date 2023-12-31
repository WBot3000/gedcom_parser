#US35
#List recent births
import unittest
from datetime import datetime, timedelta
from classes.GEDCOM_Reporting import Report, ReportDetail
from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family

class TestRecentBirths(unittest.TestCase):
    def test_recent_births_within_threshold(self):
        # Create a Report instance
        report = Report()

        # Create individuals with birth dates within the threshold
        recent_birth1 = self.create_individual('I1', 'John Doe', 'M', (datetime.today() - timedelta(days=5)).date())
        recent_birth2 = self.create_individual('I2', 'Jane Smith', 'F', (datetime.today() - timedelta(days=10)).date())
        recent_birth3 = self.create_individual('I3', 'Tom Brown', 'M', (datetime.today() - timedelta(days=25)).date())

        # Add individuals to the report
        report.indi_map = {
            'I1': recent_birth1,
            'I2': recent_birth2,
            'I3': recent_birth3,
        }

        # Call the function to update recent births within the report
        report.list_recent_births(days_threshold=20)

        # Assert that the recent births field is as expected
        self.assertEqual(len(report.recent_births), 2)
        self.assertEqual(report.recent_births[0].detailType, "I2")
        self.assertEqual(report.recent_births[1].detailType, "I1")

    def create_individual(self, id, name, sex, birth_date):
        return Individual(id, name, sex, birth_date, None, None, [])
