#US35
#List recent births
import unittest
from datetime import datetime, timedelta
from your_gedcom_parser import GEDCOMParser  # Import your GEDCOM parser class

class ListRecentBirthsTests(unittest.TestCase):
    def test_no_recent_births(self):
        parser = GEDCOMParser()
        # Create individuals with no recent births
        individual1 = Individual("I1", "John /Doe/", "M", datetime(1990, 1, 1))
        individual2 = Individual("I2", "Jane /Doe/", "F", datetime(1985, 3, 15))
        parser.individuals["I1"] = individual1
        parser.individuals["I2"] = individual2

        recent_births = parser.list_recent_births(days_threshold=30)

        self.assertEqual(len(recent_births), 0)

    def test_recent_births(self):
        parser = GEDCOMParser()
        # Create individuals with recent births
        current_date = datetime.now()
        recent_birth_date = current_date - timedelta(days=15)
        individual1 = Individual("I1", "John /Doe/", "M", recent_birth_date)
        individual2 = Individual("I2", "Jane /Doe/", "F", datetime(1995, 5, 10))
        parser.individuals["I1"] = individual1
        parser.individuals["I2"] = individual2

        recent_births = parser.list_recent_births(days_threshold=30)

        self.assertEqual(len(recent_births), 1)
        self.assertEqual(recent_births[0].id, "I1")

if __name__ == '__main__':
    unittest.main()
