import unittest
from datetime import date
from classes.GEDCOM_Reporting import Report
from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family

class US10_Tests(unittest.TestCase):
    def test_marriage_after_14_no_error (self):
        testReport: Report = Report()
        husband = Individual ("I1", "Jon Snow", "M", date(1971, 2, 23))
        wife = Individual ("I2", "Dany Tar", "F", date(1967, 12, 28))
        family = Family ("F1", husband.id, wife.id)
        family.marriageDate = date(1989, 11, 26)

        testReport.addToReport(husband)
        testReport.addToReport(wife)
        testReport.addToReport(family)

        testReport.marriage_after_14()
        self.assertEqual(len(testReport.errors), 0)

    def test_marriage_after_14_husband_error (self):
        testReport: Report = Report()
        husband = Individual ("I1", "Jon Snow", "M", date(1971, 2, 23))
        wife = Individual ("I2", "Dany Tar", "F", date(1963, 12, 28))
        family = Family ("F1", husband.id, wife.id)
        family.marriageDate = date(1979, 11, 26)

        testReport.addToReport(husband)
        testReport.addToReport(wife)
        testReport.addToReport(family)

        testReport.marriage_after_14()
        self.assertEqual(testReport.errors[0].message, "Marriage for I1 (1979-11-26) occurs before 14 (1971-02-23)")

    def test_marriage_after_14_wife_error (self):
        testReport: Report = Report()
        husband = Individual ("I1", "Jon Snow", "M", date(1961, 2, 23))
        wife = Individual ("I2", "Dany Tar", "F", date(1973, 12, 28))
        family = Family ("F1", husband.id, wife.id)
        family.marriageDate = date(1979, 11, 26)

        testReport.addToReport(husband)
        testReport.addToReport(wife)
        testReport.addToReport(family)

        testReport.marriage_after_14()
        self.assertEqual(testReport.errors[0].message, "Marriage for I2 (1979-11-26) occurs before 14 (1973-12-28)")