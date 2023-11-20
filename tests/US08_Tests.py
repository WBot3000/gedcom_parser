import unittest
from datetime import date
from classes.GEDCOM_Reporting import Report
from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family

class US08_Tests(unittest.TestCase):
    def test_check_birth_after_parents_marriage_error (self):
        testReport: Report = Report()
        husband = Individual ("I1", "Jon", "M", date(1970, 11, 2))
        wife = Individual ("I2", "Dany", "F", date(1983, 4, 8))
        child = Individual("I3", "Dragon", "F", date(2007, 1, 29))
        family = Family ("F1", husband.id, wife.id, [child.id], date(2008, 4, 3), None)
        testReport.addToReport(husband)
        testReport.addToReport(wife)
        testReport.addToReport(child)
        testReport.addToReport(family)

        testReport.check_birth_after_parents_marriage()
        self.assertEqual(testReport.anomalies[0].message, "Birth of I3 (2007-01-29) occured before marriage of parents (2008-04-03)")

    def test_check_birth_after_parents_marriage_no_error (self):
        testReport: Report = Report()
        husband = Individual ("I1", "Jon", "M", date(1970, 11, 2))
        wife = Individual ("I2", "Dany", "F", date(1983, 4, 8))
        child = Individual("I3", "Dragon", "F", date(2007, 1, 29))
        family = Family ("F1", husband.id, wife.id, [child.id], date(2004, 4, 3), None)

        testReport.addToReport(husband)
        testReport.addToReport(wife)
        testReport.addToReport(child)
        testReport.addToReport(family)

        testReport.check_birth_after_parents_marriage()
        self.assertEqual(len(testReport.anomalies), 0)


    def test_check_birth_after_parents_marriage_divorce_error (self):
        testReport: Report = Report()
        husband = Individual ("I1", "Jon", "M", date(1970, 11, 2))
        wife = Individual ("I2", "Dany", "F", date(1983, 4, 8))
        child = Individual("I3", "Dragon", "F", date(2007, 1, 29))
        family = Family ("F1", husband.id, wife.id, [child.id], date(2004, 4, 3), date(2006, 4, 3))

        testReport.addToReport(husband)
        testReport.addToReport(wife)
        testReport.addToReport(child)
        testReport.addToReport(family)

        testReport.check_birth_after_parents_marriage()
        self.assertEqual(testReport.anomalies[0].message, "Birth of I3 (2007-01-29) occured after 9 months after divorce of parents (2006-04-03)")