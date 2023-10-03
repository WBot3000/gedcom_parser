import unittest
from datetime import date
from classes.GEDCOM_Reporting import Report, ReportDetail
from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family

class US02_Tests(unittest.TestCase):
    def test_birth_after_marriage_no_error (self):
        testReport: Report = Report()
        husband = Individual ("I1", "Jon Snow", "M", date(1971, 2, 23))
        wife = Individual ("I2", "Dany Tar", "F", date(1967, 12, 28))
        family = Family ("F1", husband.id, wife.id)
        family.marriageDate = date(1989, 11, 26)

        testReport.addToMap(husband)
        testReport.addToMap(wife)
        testReport.addToMap(family)

        testReport.birth_before_marriage()
        self.assertEqual(len(testReport.errors), 0)

    def test_husband_birth_after_marriage_error (self):
        testReport: Report = Report()
        husband = Individual ("I1", "Jon Snow", "M", date(1971, 2, 23))
        wife = Individual ("I2", "Dany Tar", "F", date(1967, 12, 28))
        family = Family ("F1", husband.id, wife.id)
        family.marriageDate = date(1969, 11, 26)

        testReport.addToMap(husband)
        testReport.addToMap(wife)
        testReport.addToMap(family)

        testReport.birth_before_marriage()
        self.assertEqual(testReport.errors[0].message, "Birth of I1 (1971-02-23) occurred after their marriage (1969-11-26)")

    def test_wife_birth_after_marriage_error (self):
        testReport: Report = Report()
        husband = Individual ("I1", "Jon Snow", "M", date(1961, 2, 23))
        wife = Individual ("I2", "Dany Tar", "F", date(1967, 12, 28))
        family = Family ("F1", husband.id, wife.id)
        family.marriageDate = date(1965, 11, 26)

        testReport.addToMap(husband)
        testReport.addToMap(wife)
        testReport.addToMap(family)

        testReport.birth_before_marriage()
        self.assertEqual(testReport.errors[0].message, "Birth of I2 (1967-12-28) occurred after their marriage (1965-11-26)")

    def test_husband_wife_birth_after_marriage_error (self):
        testReport: Report = Report()
        husband = Individual ("I1", "Jon Snow", "M", date(1971, 2, 23))
        wife = Individual ("I2", "Dany Tar", "F", date(1967, 12, 28))
        family = Family ("F1", husband.id, wife.id)
        family.marriageDate = date(1959, 11, 26)

        testReport.addToMap(husband)
        testReport.addToMap(wife)
        testReport.addToMap(family)

        testReport.birth_before_marriage()
        self.assertEqual(testReport.errors[0].message, "Birth of I1 (1971-02-23) occurred after their marriage (1959-11-26)")

    def test_wife_birth_same_marriage_no_error (self):
        testReport: Report = Report()
        husband = Individual ("I1", "Jon Snow", "M", date(1965, 2, 23))
        wife = Individual ("I2", "Dany Tar", "F", date(1967, 10, 28))
        family = Family ("F1", husband.id, wife.id)
        family.marriageDate = date(1967, 11, 26)

        testReport.addToMap(husband)
        testReport.addToMap(wife)
        testReport.addToMap(family)

        testReport.birth_before_marriage()
        self.assertEqual(len(testReport.errors), 0)