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

        testReport.marriage_after_14()
        self.assertEqual(len(testReport.errors), 0)