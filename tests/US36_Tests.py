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
        recent_death1 = self.create_individual('I1', 'John Doe', 'M', self.today - timedelta(days=15))
        recent_death2 = self.create_individual('I2', 'Jane Smith', 'F', self.today - timedelta(days=10))
        recent_death3 = self.create_individual('I3', 'Tom Brown', 'M', self.today - timedelta(days=25))

        # Add individuals to the report
        report.individuals = {
            'I1': recent_death1,
            'I2': recent_death2,
            'I3': recent_death3,
        }

        # Call the function to update recent deaths within the report
        report.list_recent_deaths(days_threshold=20)

        # Assert that the recent deaths field is as expected
        self.assertEqual(len(report.recent_deaths), 2)
        self.assertTrue(all(individual in report.recent_deaths for individual in [recent_death1, recent_death2]))

    def create_individual(self, id, name, sex, death_date):
        individual = self.create_individual(id)
        individual.name = name
        individual.sex = sex
        individual.death_date = death_date
        return individual
