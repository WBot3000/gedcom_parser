import unittest
from datetime import date
from classes.GEDCOM_Reporting import Report, ReportDetail
from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family

class US05_Tests(unittest.TestCase):
    def test_marriage_before_death_no_error(self):
        testReport: Report = Report()
        individual = Individual("I1", "Jon Snow", "M", date(1980, 5, 15), date(2020, 3, 10))
        family = Family("F1", "I1", None, None, date(2010, 6, 15), None)

        testReport.addToReport(individual)
        testReport.addToReport(family)

        testReport.marriage_before_death()
        self.assertEqual(len(testReport.errors), 0)


    def test_marriage_after_death_error(self):
        testReport: Report = Report()
        individual = Individual("I1", "Jon Snow", "M", date(1980, 5, 15), date(2018, 2, 5))
        family = Family("F1", "I1", None, None, date(2020, 3, 10), None)

        testReport.addToReport(individual)
        testReport.addToReport(family)

        testReport.marriage_before_death()
        self.assertEqual(testReport.errors[0].detailType, "Marriage After Death")
        self.assertEqual(testReport.errors[0].message, "Marriage of F1 (2020-03-10) occurs after the death of Jon Snow (2018-02-05)")


    def test_same_marriage_and_death_dates_no_error(self):
        testReport: Report = Report()
        individual = Individual("I1", "Jon Snow", "M", date(1980, 5, 15), date(2020, 3, 10))
        family = Family("F1", "I1", None, None, date(2020, 3, 10), None)

        testReport.addToReport(individual)
        testReport.addToReport(family)

        testReport.marriage_before_death()
        self.assertEqual(len(testReport.errors), 0)