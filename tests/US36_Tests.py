#US36 - List recent deaths 
import unittest
from datetime import datetime, date, timedelta
from classes.GEDCOM_Reporting import Report, ReportDetail
from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family

class TestRecentDeaths(unittest.TestCase):
    def test_recent_deaths_within_threshold(self):
        # Create a Report instance
        report = Report()

        # Create individuals with death dates within the threshold
        recent_death1 = self.create_individual('I1', 'John Doe', 'M', (datetime.today() - timedelta(days=15)).date())
        recent_death2 = self.create_individual('I2', 'Jane Smith', 'F', (datetime.today() - timedelta(days=10)).date())
        recent_death3 = self.create_individual('I3', 'Tom Brown', 'M', (datetime.today() - timedelta(days=25)).date())

        # Add individuals to the report
        report.indi_map = {
            'I1': recent_death1,
            'I2': recent_death2,
            'I3': recent_death3,
        }

        # Call the function to update recent deaths within the report
        report.list_recent_deaths(days_threshold=20)

        # Assert that the recent deaths field is as expected
        self.assertEqual(len(report.recent_deaths), 2)
        self.assertEqual(report.recent_deaths[0].detailType, "I1")
        self.assertEqual(report.recent_deaths[1].detailType, "I2")

    def create_individual(self, id, name, sex, death_date):
        return Individual(id, name, sex, None, death_date, None, [])
