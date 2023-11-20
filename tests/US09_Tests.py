import unittest
from datetime import date
from classes.GEDCOM_Reporting import Report
from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family

class US09_Tests(unittest.TestCase):
    def test_check_birth_before_death_mother_error (self):
        testReport: Report = Report()
        husband = Individual ("I1", "Jon", "M", date(1970, 11, 2))
        wife = Individual ("I2", "Dany", "F", date(1983, 4, 8), date(2007, 1, 28))
        child = Individual("I3", "Dragon", "F", date(2007, 1, 29))
        family = Family ("F1", husband.id, wife.id, [child.id], None, None)
        testReport.addToReport(husband)
        testReport.addToReport(wife)
        testReport.addToReport(child)
        testReport.addToReport(family)

        testReport.check_birth_before_death_parents()
        self.assertEqual(testReport.errors[0].message, "Birth of I3 (2007-01-29) occured after death of mother (2007-01-28)")

    def test_check_birth_before_death_mother_no_error (self):
        testReport: Report = Report()
        husband = Individual ("I1", "Jon", "M", date(1970, 11, 2), date(2009, 1, 29))
        wife = Individual ("I2", "Dany", "F", date(1983, 4, 8))
        child = Individual("I3", "Dragon", "F", date(2007, 1, 29))
        family = Family ("F1", husband.id, wife.id, [child.id], date(2004, 4, 3), None)

        testReport.addToReport(husband)
        testReport.addToReport(wife)
        testReport.addToReport(child)
        testReport.addToReport(family)

        testReport.check_birth_before_death_parents()
        self.assertEqual(len(testReport.errors), 0)
    
    def test_check_birth_before_death_father_no_error (self):
        testReport: Report = Report()
        husband = Individual ("I1", "Jon", "M", date(1970, 11, 2))
        wife = Individual ("I2", "Dany", "F", date(1983, 4, 8), date(2009, 1, 29))
        child = Individual("I3", "Dragon", "F", date(2007, 1, 29))
        family = Family ("F1", husband.id, wife.id, [child.id], date(2004, 4, 3), None)

        testReport.addToReport(husband)
        testReport.addToReport(wife)
        testReport.addToReport(child)
        testReport.addToReport(family)

        testReport.check_birth_before_death_parents()
        self.assertEqual(len(testReport.errors), 0)

    def test_check_birth_before_death_parents_no_error (self):
        testReport: Report = Report()
        husband = Individual ("I1", "Jon", "M", date(1970, 11, 2), date(2009, 1, 29))
        wife = Individual ("I2", "Dany", "F", date(1983, 4, 8), date(2009, 1, 29))
        child = Individual("I3", "Dragon", "F", date(2007, 1, 29))
        family = Family ("F1", husband.id, wife.id, [child.id], date(2004, 4, 3), None)

        testReport.addToReport(husband)
        testReport.addToReport(wife)
        testReport.addToReport(child)
        testReport.addToReport(family)

        testReport.check_birth_before_death_parents()
        self.assertEqual(len(testReport.errors), 0)

    def test_check_birth_before_death_father_error (self):
        testReport: Report = Report()
        husband = Individual ("I1", "Jon", "M", date(1970, 11, 2), date(2006, 1, 29))
        wife = Individual ("I2", "Dany", "F", date(1983, 4, 8))
        child = Individual("I3", "Dragon", "F", date(2007, 1, 29))
        family = Family ("F1", husband.id, wife.id, [child.id], date(2004, 4, 3), date(2006, 4, 3))

        testReport.addToReport(husband)
        testReport.addToReport(wife)
        testReport.addToReport(child)
        testReport.addToReport(family)

        testReport.check_birth_before_death_parents()
        self.assertEqual(testReport.errors[0].message, "Birth of I3 (2007-01-29) occured after 9 months after death of father (2006-01-29)")