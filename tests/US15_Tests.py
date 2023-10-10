#US15_FEWER THAN 15 SIBLINGS
import unittest
from classes.GEDCOM_Units import Individual, Family
from classes.Report import Report

class TestFewerThan15Siblings(unittest.TestCase):
    def test_fewer_than_15_siblings_no_issues(self):
        # Create a report instance
        report = Report()

        # Create a family with 10 children
        fam = Family("F1")
        fam.childIds = ["I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8", "I9", "I10"]
        report.fam_map["F1"] = fam

        # Check for fewer than 15 siblings
        report.fewer_than_15_siblings()

        # Assert that no errors were added to the report
        self.assertEqual(len(report.errors), 0)

    def test_fewer_than_15_siblings_15_or_more_siblings(self):
        # Create a report instance
        report = Report()

        # Create a family with 15 children
        fam = Family("F1")
        fam.childIds = ["I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8", "I9", "I10", "I11", "I12", "I13", "I14", "I15"]
        report.fam_map["F1"] = fam

        # Check for fewer than 15 siblings
        report.fewer_than_15_siblings()

        # Assert that an error was added to the report
        self.assertEqual(len(report.errors), 1)
        self.assertEqual(report.errors[0].detailType, "Too Many Siblings")
