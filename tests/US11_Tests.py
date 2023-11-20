import unittest
from datetime import date, datetime
from classes.GEDCOM_Reporting import Report, ReportDetail
from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family

class US11_Tests(unittest.TestCase):
    def test_check_bigamy_no_error (self):
        testReport: Report = Report()
        husband = Individual ("I1", "Jon Snow", "M", date(1971, 2, 23))
        wife = Individual ("I2", "Rose", "F", date(1973, 12, 28))
        wife2 = Individual("I3", "Dany T", "F", date(1961, 4, 21))
        family = Family ("F1", husband.id, wife.id)
        family.marriageDate = date(1989, 5, 30)
        family.divorceDate = date(1997, 11, 25)
        family2 = Family ("F2", husband.id, wife2.id)
        family2.marriageDate = date(1999, 2, 12)

        testReport.addToReport(husband)
        testReport.addToReport(wife)
        testReport.addToReport(family)
        testReport.addToReport(wife2)
        testReport.addToReport(family2)

        testReport.check_bigamy()
        self.assertEqual(len(testReport.errors), 0)
    
    def test_check_bigamy_husband_error (self):
        testReport: Report = Report()
        husband = Individual ("I1", "Jon Snow", "M", date(1971, 2, 23), None, None, ["F1", "F2"])
        wife = Individual ("I2", "Rose", "F", date(1973, 12, 28), None, None, ["F1"])
        wife2 = Individual("I3", "Dany T", "F", date(1961, 4, 21), None, None, ["F2"])
        family = Family ("F1", husband.id, wife.id, None, date(1989, 5, 30), date(1997, 11, 25))
        family2 = Family ("F2", husband.id, wife2.id, None, date(1996, 2, 12), None)

        testReport.addToReport(husband)
        testReport.addToReport(wife)
        testReport.addToReport(family)
        testReport.addToReport(wife2)
        testReport.addToReport(family2)

        testReport.check_bigamy()
        self.assertEqual(testReport.errors[0].message, "Spouse details are: I1 and families are F1 and F2")

    def test_check_bigamy_wife_error (self):
        testReport: Report = Report()
        husband1 = Individual ("I1", "Jon Snow", "M", date(1971, 2, 23), None, None, ["F1"])
        wife = Individual ("I2", "Rose", "F", date(1973, 12, 28), None, None, ["F1", "F2"])
        husband2 = Individual("I3", "Dan T", "M", date(1961, 4, 21), None, None, ["F2"])
        family = Family ("F1", husband1.id, wife.id, None, date(1989, 5, 30), date(1997, 11, 25))
        family2 = Family ("F2", husband2.id, wife.id, None, date(1996, 2, 12), None)

        testReport.addToReport(husband1)
        testReport.addToReport(wife)
        testReport.addToReport(family)
        testReport.addToReport(husband2)
        testReport.addToReport(family2)

        testReport.check_bigamy()
        self.assertEqual(testReport.errors[0].message, "Spouse details are: I2 and families are F1 and F2")