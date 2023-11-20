import unittest
from datetime import date
from classes.GEDCOM_Reporting import Report, ReportDetail
from classes.GEDCOM_Units import GEDCOMUnit, Individual

class US07_Tests(unittest.TestCase):
    def test_valid_ages(self):
        testReport: Report = Report()
        indiA: Individual = Individual("a", "John /Doe/", "M", date(1990, 1, 1))
        testReport.addToReport(indiA)
        testReport.check_max_age()
        self.assertEqual(testReport.errors, [], "Test Report has errors, despite all people being 150 years old or less")


    def test_too_old_alive(self):
        testReport: Report = Report()
        indi: Individual = Individual("a", "John /Doe/", "M", date(1800, 1, 1))
        testReport.addToReport(indi)
        testReport.check_max_age()
        self.assertEqual(testReport.errors, [ReportDetail("Over 150 Years Old", f"a is over 150 years old ({indi.calculateAge()} years old)")], f"Test Report has no errors, despite the user being {indi.calculateAge()} years old")


    def test_too_old_deceased(self):
        testReport: Report = Report()
        indi: Individual = Individual("a", "Ol' Johnny /Doesph/", "M", date(1700, 1, 1), date(1900, 2, 2))
        testReport.addToReport(indi)
        testReport.check_max_age()
        self.assertEqual(testReport.errors, [ReportDetail("Over 150 Years Old", f"a is over 150 years old ({indi.calculateAge()} years old)")], f"Test Report has no errors, despite the user being {indi.calculateAge()} years old")


    def test_too_old_alive_no_bday(self):
        testReport: Report = Report()
        indi: Individual = Individual("a", "Jane /Doe/", "F", None)
        testReport.addToReport(indi)
        testReport.check_max_age()
        self.assertEqual(testReport.errors, [], "Test Report has errors, despite the user not having a birthdate (while alive)")

    def test_too_old_deceased_no_bday(self):
        testReport: Report = Report()
        indi: Individual = Individual("a", "Ol' Janine /Doesph/", "F", None, date(2005, 9, 3))
        testReport.addToReport(indi)
        testReport.check_max_age()
        self.assertEqual(testReport.errors, [], "Test Report has errors, despite the user not having a birthdate (while deceased)")