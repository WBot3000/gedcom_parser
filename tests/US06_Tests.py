import unittest
from datetime import date
from classes.GEDCOM_Reporting import Report, ReportDetail
from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family

class US06_Tests(unittest.TestCase):
    def test_divorce_before_death_no_error(self):
        testReport: Report = Report()
        individual = Individual("I1", "Jon Snow", "M", date(1980, 5, 15), date(2020, 3, 10), None, "F1")
        family = Family("F1", "I1", None, None, date(2000, 1, 1), date(2019, 6, 30))

        testReport.addToReport(individual)
        testReport.addToReport(family)

        testReport.divorce_before_death()
        self.assertEqual(len(testReport.errors), 0)

    def test_divorce_after_death_error(self):
        testReport: Report = Report()
        individual = Individual("I1", "Jon Snow", "M", date(1980, 5, 15), date(2018, 2, 5), None, "F1")
        family = Family("F1", "I1", None, None, date(2000, 1, 1), date(2020, 3, 10))

        testReport.addToReport(individual)
        testReport.addToReport(family)

        testReport.divorce_before_death()
        self.assertEqual(testReport.errors[0].detailType, "Divorce After Death")
        self.assertEqual(testReport.errors[0].message, "Divorce for family F1 (2020-03-10) occurs after the death of the husband (2018-02-05)")

    def test_death_before_divorce_no_error(self):
        testReport: Report = Report()
        individual = Individual("I1", "Jon Snow", "M", date(1980, 5, 15), date(2020, 3, 10), None, "F1")
        family = Family("F1", "I1", None, None, date(2000, 1, 1), date(2017, 12, 5))

        testReport.addToReport(individual)
        testReport.addToReport(family)

        testReport.divorce_before_death()
        self.assertEqual(len(testReport.errors), 0)

    def test_same_divorce_and_death_dates_no_error(self):
        testReport: Report = Report()
        individual = Individual("I1", "Jon Snow", "M", date(1980, 5, 15), date(2020, 3, 10), None, "F1")
        family = Family("F1", "I1", None, None, date(2000, 1, 1), date(2020, 3, 10))

        testReport.addToReport(individual)
        testReport.addToReport(family)

        testReport.divorce_before_death()
        self.assertEqual(len(testReport.errors), 0)