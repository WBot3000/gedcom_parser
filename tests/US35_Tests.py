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
        recent_birth1 = self.create_individual('I1', 'John Doe', 'M', self.today - timedelta(days=5))
        recent_birth2 = self.create_individual('I2', 'Jane Smith', 'F', self.today - timedelta(days=10))
        recent_birth3 = self.create_individual('I3', 'Tom Brown', 'M', self.today - timedelta(days=25))

        # Add individuals to the report
        report.individuals = {
            'I1': recent_birth1,
            'I2': recent_birth2,
            'I3': recent_birth3,
        }

        # Call the function to update recent births within the report
        report.list_recent_births(days_threshold=20)

        # Assert that the recent births field is as expected
        self.assertEqual(len(report.recent_births), 2)
        self.assertTrue(all(individual in report.recent_births for individual in [recent_birth1, recent_birth2]))

    def create_individual(self, id, name, sex, birth_date):
        individual = self.create_individual(id)
        individual.name = name
        individual.sex = sex
        individual.birth_date = birth_date
        return individual
