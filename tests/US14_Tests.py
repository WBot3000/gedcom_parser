import unittest
from datetime import date
from classes.GEDCOM_Reporting import Report, ReportDetail
from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family

class US14_Tests(unittest.TestCase):
    def test_multiple_births_no_error(self):
        testReport: Report = Report()
        individual1 = Individual("I1", "Child1", "M", date(1990, 1, 1), None)
        individual2 = Individual("I2", "Child2", "F", date(1991, 2, 2), None)
        individual3 = Individual("I3", "Child3", "M", date(1992, 3, 3), None)
        individual4 = Individual("I4", "Child4", "F", date(1993, 4, 4), None)
        individual5 = Individual("I5", "Child5", "M", date(1994, 5, 5), None)
        family1 = Family("F1", None, None, ["I1", "I2", "I3", "I4", "I5"])

        testReport.addToReport(individual1)
        testReport.addToReport(individual2)
        testReport.addToReport(individual3)
        testReport.addToReport(individual4)
        testReport.addToReport(individual5)
        testReport.addToReport(family1)

        testReport.check_multiple_births()
        self.assertEqual(len(testReport.errors), 0)

    def test_multiple_births_equal_to_5_no_error(self):
        testReport: Report = Report()
        individual1 = Individual("I1", "Child1", "M", date(1990, 1, 1), None)
        individual2 = Individual("I2", "Child2", "F", date(1990, 1, 1), None)
        individual3 = Individual("I3", "Child3", "M", date(1990, 1, 1), None)
        individual4 = Individual("I4", "Child4", "F", date(1990, 1, 1), None)
        individual5 = Individual("I5", "Child5", "M", date(1990, 1, 1), None)
        family1 = Family("F1", None, None, ["I1", "I2", "I3", "I4", "I5"])

        testReport.addToReport(individual1)
        testReport.addToReport(individual2)
        testReport.addToReport(individual3)
        testReport.addToReport(individual4)
        testReport.addToReport(individual5)
        testReport.addToReport(family1)

        testReport.check_multiple_births()
        self.assertEqual(len(testReport.anomalies), 0)

    def test_multiple_births_over_5_error(self):
        testReport: Report = Report()
        individual1 = Individual("I1", "Child1", "M", date(1990, 1, 1), None)
        individual2 = Individual("I2", "Child2", "F", date(1990, 1, 1), None)
        individual3 = Individual("I3", "Child3", "M", date(1990, 1, 1), None)
        individual4 = Individual("I4", "Child4", "F", date(1990, 1, 1), None)
        individual5 = Individual("I5", "Child5", "M", date(1990, 1, 1), None)
        individual6 = Individual("I6", "Child6", "F", date(1990, 1, 1), None)
        family1 = Family("F1", None, None, ["I1", "I2", "I3", "I4", "I5", "I6"])

        testReport.addToReport(individual1)
        testReport.addToReport(individual2)
        testReport.addToReport(individual3)
        testReport.addToReport(individual4)
        testReport.addToReport(individual5)
        testReport.addToReport(individual6)
        testReport.addToReport(family1)

        testReport.check_multiple_births()
        self.assertEqual(testReport.anomalies[0].message, "More than five siblings were born on 1990-01-01 in family F1.")