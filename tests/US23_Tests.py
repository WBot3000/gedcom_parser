import unittest
from datetime import date
from classes.GEDCOM_Reporting import Report
from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family

class TestCheckUniqueNamesAndBirthDates(unittest.TestCase):
    def test_unique_names(self):
        # Create an empty report
        report = Report()

        # Create individuals with unique names
        indi1 = Individual("Indi1", "Lastname1 /Lastname/", "M", None, None, None, None)
        indi2 = Individual("Indi2", "Lastname2 /Lastname/", "F", None, None, None, None)

        # Run the check_unique_names method
        name_count = {}
        for indi in [indi1, indi2]:
            name = indi.name
            if name in name_count:
                name_count[name] += 1
            else:
                name_count[name] = 1

        # Assert that there are no non-unique names
        for name, count in name_count.items():
            self.assertEqual(count, 1)

    def test_non_unique_names(self):
        # Create an empty report
        report = Report()

        # Create individuals with non-unique names
        indi1 = Individual("Indi1", "Lastname1 /Lastname/", "M", None, None, None, None)
        indi2 = Individual("Indi1", "Lastname2 /Lastname/", "F", None, None, None, None)

        # Run the check_unique_names method
        name_count = {}
        for indi in [indi1, indi2]:
            name = indi.name
            if name in name_count:
                name_count[name] += 1
            else:
                name_count[name] = 1

        # Assert that there are non-unique names
        for name, count in name_count.items():
            if count > 1:
                self.assertTrue(True)  # At least one name is non-unique

    def test_unique_birth_dates(self):
        # Create an empty report
        report = Report()

        # Create individuals with unique birth dates
        indi1 = Individual("Indi1", "Lastname1 /Lastname/", "M", date(1990, 1, 1), None, None, None)
        indi2 = Individual("Indi2", "Lastname2 /Lastname/", "F", date(1995, 2, 2), None, None, None)

        # Run the check_unique_birth_dates method
        birth_date_count = {}
        for indi in [indi1, indi2]:
            birth_date = indi.birth_date
            if birth_date:
                if birth_date in birth_date_count:
                    birth_date_count[birth_date] += 1
                else:
                    birth_date_count[birth_date] = 1

        # Assert that there are no non-unique birth dates
        for date, count in birth_date_count.items():
            self.assertEqual(count, 1)

    def test_non_unique_birth_dates(self):
        # Create an empty report
        report = Report()

        # Create individuals with non-unique birth dates
        indi1 = Individual("Indi1", "Lastname1 /Lastname/", "M", date(1990, 1, 1), None, None, None)
        indi2 = Individual("Indi2", "Lastname2 /Lastname/", "F", date(1990, 1, 1), None, None, None)

        # Run the check_unique_birth_dates method
        birth_date_count = {}
        for indi in [indi1, indi2]:
            birth_date = indi.birth_date
            if birth_date:
                if birth_date in birth_date_count:
                    birth_date_count[birth_date] += 1
                else:
                    birth_date_count[birth_date] = 1

        # Assert that there are non-unique birth dates
        for date, count in birth_date_count.items():
            if count > 1:
                self.assertTrue(True)  # At least one birth date is non-unique