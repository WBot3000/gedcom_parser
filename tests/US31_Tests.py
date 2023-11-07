import unittest
from datetime import date
from classes.GEDCOM_Reporting import Report, ReportDetail
from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family

class US31_Tests(unittest.TestCase):
    def test_check_single_status_false (self):
        testReport = Report()
        husband = Individual("I1", "Child1", "M", None, None, None, ["F1"])
        wife = Individual ("I2", "Dany Tar", "F", None, None, None, ["F1"])
        family = Family("F1", husband.id, wife.id, [], None, None)

        testReport.addToReport(husband)
        testReport.addToReport(wife)
        testReport.addToReport(family)

        result = testReport.check_single_status(husband)
        self.assertEqual(result, False)
    
    def test_check_single_status_true (self):
        testReport = Report()
        Indi1 = Individual("I1", "Jon Snow", "M", date(2021, 2, 2), None, None, [])

        testReport.addToReport(Indi1)

        result = testReport.check_single_status(Indi1)
        self.assertEqual(result, True)