import unittest
from datetime import date, timedelta, datetime
from classes.GEDCOM_Reporting import Report
from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family

class TestUpcomingAnniversaries(unittest.TestCase):
    def test_upcoming_anniversaries_within_threshold(self):
        # Create a Report instance
        test_report = Report()

        # Create individuals with birth and marriage dates
        husband = self.create_individual('I1', 'John Doe', 'M', date(1970, 1, 1))
        wife = self.create_individual('I2', 'Jane Smith', 'F', date(1975, 5, 10))

        # Create a family with a marriage date within the threshold
        upcoming_anniversary_date = (datetime.now() + timedelta(10)).date()
        upcoming_anniversary_family = self.create_family('F1', husband.id, wife.id, upcoming_anniversary_date)

        # Add individuals and families to the GEDCOMUnit
        test_report.indi_map = {
            'I1': husband,
            'I2': wife,
        }

        test_report.fam_map = {
            'F1': upcoming_anniversary_family,
        }

        # Call the function to list upcoming anniversaries
        upcoming_anniversaries = test_report.list_upcoming_anniversaries(days_threshold=30)

        # Assert that the upcoming anniversaries list is as expected
        self.assertEqual(len(upcoming_anniversaries), 1)
        # Add assertions based on your expectations for the anniversary details
        self.assertEqual(upcoming_anniversaries[0][0], 'F1')


    def test_upcoming_anniversaries_outside_threshold(self):
        # Create a Report instance
        test_report = Report()

        # Create individuals with birth and marriage dates
        husband = self.create_individual('I1', 'John Doe', 'M', datetime(1970, 1, 1).date())
        wife = self.create_individual('I2', 'Jane Smith', 'F', datetime(1975, 5, 10).date())

        # Create a family with a marriage date outside the threshold
        past_anniversary_date = (datetime.now() - timedelta(10)).date()
        past_anniversary_family = self.create_family('F1', husband.id, wife.id, past_anniversary_date)

        # Add individuals and families to the Report
        test_report.indi_map = {
            'I1': husband,
            'I2': wife,
        }

        test_report.fam_map = {
            'F1': past_anniversary_family,
        }

        # Call the function to list upcoming anniversaries
        upcoming_anniversaries = test_report.list_upcoming_anniversaries(days_threshold=30)

        # Assert that the upcoming anniversaries list is empty
        self.assertEqual(len(upcoming_anniversaries), 0)


    def test_upcoming_anniversaries_with_divorce(self):
        # Create a Report instance
        test_report = Report()

        # Create individuals with birth and marriage dates
        husband = self.create_individual('I1', 'John Doe', 'M', date(1970, 1, 1))
        wife = self.create_individual('I2', 'Jane Smith', 'F', date(1975, 5, 10))

        # Create a family with a marriage date and divorce date
        divorced_anniversary_date = (datetime.now() + timedelta(10)).date()
        divorced_family = self.create_family('F1', husband.id, wife.id, divorced_anniversary_date)
        divorced_family.divorceDate = datetime(2010, 11, 25).date()

        # Add individuals and families to the Report
        test_report.indi_map = {
            'I1': husband,
            'I2': wife,
        }

        test_report.fam_map = {
            'F1': divorced_family,
        }

        # Call the function to list upcoming anniversaries
        upcoming_anniversaries = test_report.list_upcoming_anniversaries(days_threshold=30)

        # Assert that the upcoming anniversaries list is empty
        self.assertEqual(len(upcoming_anniversaries), 0)


    def create_individual(self, id, name, sex, birth_date):
        return Individual(id, name, sex, birth_date, None, None, [])

    def create_family(self, id, husband_id, wife_id, marriage_date):
        return Family(id, husband_id, wife_id, [], marriage_date, None)
