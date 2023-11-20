import unittest
from datetime import date
from classes.GEDCOM_Reporting import Report
from classes.GEDCOM_Units import Individual, Family

class TestLargeAgeDifference(unittest.TestCase):
    def test_couples_with_large_age_difference(self):
        # Create a GEDCOMUnit instance
        test_report = Report()

        # Create individuals with birth dates
        husband = self.create_individual('I1', 'John Doe', 'M', date(1950, 1, 1))
        wife = self.create_individual('I2', 'Jane Smith', 'F', date(1990, 1, 1))

        # Create a family with a large age difference
        large_age_family = self.create_family('F1', husband.id, wife.id, date(2000, 12, 10))

        # Add individuals and families to the GEDCOMUnit
        test_report.indi_map = {
            'I1': husband,
            'I2': wife,
        }

        test_report.fam_map = {
            'F1': large_age_family,
        }

        # Call the function to list couples with large age differences
        test_report.list_couples_with_large_age_difference()

        # Assert that the anomalies field is as expected
        self.assertEqual(len(test_report.anomalies), 1)
        # Add assertions based on your expectations for the anomaly details
        self.assertEqual(test_report.anomalies[0].detailType, "Large Couple Age Gap")
        

    def create_individual(self, id, name, sex, birth_date):
        return Individual(id, name, sex, birth_date, None, None, [])

    def create_family(self, id, husband_id, wife_id, marriage_date):
        return Family(id, husband_id, wife_id, [], marriage_date, None)
