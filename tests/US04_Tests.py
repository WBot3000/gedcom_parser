import unittest
from datetime import date
from classes.GEDCOM_Reporting import Report, ReportDetail
from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family

class US04_Tests(unittest.TestCase):
    def test_marriage_before_divorce_no_error(self):
        testReport: Report = Report()
        spouse1 = Individual("I1", "Jon Snow", "M", date(1980, 5, 15), date(2020, 3, 10))
        spouse2 = Individual("I2", "Daenerys Targaryen", "F", date(1985, 7, 28), date(2020, 3, 10))
        family = Family("F1", "I1", "I2", None, date(2010, 6, 15), None)

        testReport.addToReport(spouse1)
        testReport.addToReport(spouse2)
        testReport.addToReport(family)

        testReport.marriage_before_divorce()
        self.assertEqual(len(testReport.errors), 0)

    def test_marriage_after_divorce_error(self):
        testReport: Report = Report()
        spouse1 = Individual("I1", "Jon Snow", "M", date(1980, 5, 15), date(2018, 2, 5))
        spouse2 = Individual("I2", "Daenerys Targaryen", "F", date(1985, 7, 28), date(2020, 3, 10))
        family = Family("F1", "I1", "I2", None, date(2021, 1, 20), date(2019, 6, 30))

        testReport.addToReport(spouse1)
        testReport.addToReport(spouse2)
        testReport.addToReport(family)

        testReport.marriage_before_divorce()
        self.assertEqual(testReport.errors[0].message, "Divorce of F1 (2019-06-30) occurs before their marriage (2021-01-20)")

    def test_divorce_before_marriage_error(self):
        testReport: Report = Report()
        spouse1 = Individual("I1", "Jon Snow", "M", date(1980, 5, 15), date(2020, 3, 10))
        spouse2 = Individual("I2", "Daenerys Targaryen", "F", date(1985, 7, 28), date(2020, 3, 10))
        family = Family("F1", "I1", "I2", None, date(2019, 12, 5), date(2018, 6, 20))

        testReport.addToReport(spouse1)
        testReport.addToReport(spouse2)
        testReport.addToReport(family)

        testReport.marriage_before_divorce()
        self.assertEqual(testReport.errors[0].message, "Divorce of F1 (2018-06-20) occurs before their marriage (2019-12-05)")

    def test_same_marriage_and_divorce_dates_no_error(self):
        testReport: Report = Report()
        spouse1 = Individual("I1", "Jon Snow", "M", date(1980, 5, 15), date(2020, 3, 10))
        spouse2 = Individual("I2", "Daenerys Targaryen", "F", date(1985, 7, 28), date(2020, 3, 10))
        family = Family("F1", "I1", "I1", None, date(2018, 6, 30), date(2018, 6, 30))

        testReport.addToReport(spouse1)
        testReport.addToReport(spouse2)
        testReport.addToReport(family)

        testReport.marriage_before_divorce()
        self.assertEqual(len(testReport.errors), 0)