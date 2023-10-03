import unittest
from datetime import date
from classes.GEDCOM_Reporting import Report, ReportDetail
from classes.GEDCOM_Units import GEDCOMUnit, Individual

class US03_Tests(unittest.TestCase):
    def test_birth_after_death_no_error (self):
        testReport: Report = Report()
        individual = Individual ("I1", "Jon Snow", "M", date(1971, 2, 23), date(2021, 2, 23))
        
        testReport.addToMap(individual)

        testReport.birth_before_death()
        self.assertEqual(len(testReport.errors), 0)

    def test_birth_after_death_error (self):
        testReport: Report = Report()
        individual = Individual ("I1", "Jon Snow", "M", date(1971, 2, 23), date(1921, 2, 23))
        
        testReport.addToMap(individual)

        testReport.birth_before_death()
        self.assertEqual(testReport.errors[0].message, "Birth of I1 (1971-02-23) occurs after their death (1921-02-23)")

    def test_future_birth_after_death_error (self):
        testReport: Report = Report()
        individual = Individual ("I1", "Jon Snow", "M", date(2045, 2, 23), date(2021, 2, 23))
        
        testReport.addToMap(individual)

        testReport.birth_before_death()
        self.assertEqual(testReport.errors[0].message, "Birth of I1 (2045-02-23) occurs after their death (2021-02-23)")

    def test_same_birth_after_death_no_error (self):
        testReport: Report = Report()
        individual = Individual ("I1", "Jon Snow", "M", date(2021, 2, 23), date(2021, 2, 23))
        
        testReport.addToMap(individual)

        testReport.birth_before_death()
        self.assertEqual(len(testReport.errors), 0)

    def test_same_year_birth_and_death_no_error (self):
        testReport: Report = Report()
        individual = Individual ("I1", "Jon Snow", "M", date(2021, 2, 23), date(2021, 12, 23))
        
        testReport.addToMap(individual)

        testReport.birth_before_death()
        self.assertEqual(len(testReport.errors), 0)