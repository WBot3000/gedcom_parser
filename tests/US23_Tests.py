import unittest
from datetime import date
from classes.GEDCOM_Reporting import Report
from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family

class TestCheckUniqueNamesAndBirthDates(unittest.TestCase):
    def test_unique_names(self):
        # Create an empty report
        report = Report()

        # Create individuals with unique names
        indi1 = Individual("Indi1", "Lastname1 /Lastname/", "M", date(1990, 1, 1), None, None, None)
        indi2 = Individual("Indi2", "Lastname2 /Lastname/", "F", date(1990, 1, 1), None, None, None)

        report.check_unique_name_and_birth_date()

        self.assertEqual(len(report.anomalies), 0)


    def test_unique_birth_dates(self):
        # Create an empty report
        report = Report()

        # Create individuals with unique birth dates
        indi1 = Individual("Indi1", "Lastname1 /Lastname/", "M", date(1990, 1, 1), None, None, None)
        indi2 = Individual("Indi2", "Lastname1 /Lastname/", "F", date(1995, 2, 2), None, None, None)

        report.addToReport(indi1)
        report.addToReport(indi2)

        report.check_unique_name_and_birth_date()

        self.assertEqual(len(report.anomalies), 0)


    def test_non_unique_names_and_birth_dates(self):
        # Create an empty report
        report = Report()

        # Create individuals with non-unique birth dates
        indi1 = Individual("Indi1", "Lastname1 /Lastname/", "M", date(1990, 1, 1), None, None, None)
        indi2 = Individual("Indi2", "Lastname1 /Lastname/", "F", date(1990, 1, 1), None, None, None)

        report.addToReport(indi1)
        report.addToReport(indi2)

        report.check_unique_name_and_birth_date()

        self.assertEqual(len(report.anomalies), 1)
        self.assertEqual(report.anomalies[0].detailType, "Duplicate Name and Birthdate")
        self.assertEqual(report.anomalies[0].message, f"Indi1, Indi2 share a name (Lastname1 /Lastname/) and birthday (1990-01-01)")

