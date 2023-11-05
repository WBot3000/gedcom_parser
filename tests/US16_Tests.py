import unittest
from datetime import date
from classes.GEDCOM_Reporting import Report, ReportDetail
from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family

class US16_Tests(unittest.TestCase):
    def test_only_husband(self):
        testReport: Report = Report()
        husband: Individual = Individual("m1", "Jack /Person/", "M")
        family: Family = Family("F1", husband.id, None, None)

        testReport.addToReport(husband)
        testReport.addToReport(family)

        testReport.check_family_male_surnames()
        self.assertEqual(len(testReport.errors), 0)

    def test_only_child(self):
        testReport: Report = Report()
        child: Individual = Individual("m2", "Tyler /Person/", "M")
        family = Family("F1", None, None, [child.id])

        testReport.addToReport(child)
        testReport.addToReport(family)

        testReport.check_family_male_surnames()
        self.assertEqual(len(testReport.errors), 0)

    def test_shared_male_surnames(self):
        testReport: Report = Report()
        husband: Individual = Individual("m1", "Jack /Person/", "M")
        wife: Individual = Individual("f1", "Mary /Human/", "F")
        child1: Individual = Individual("m2", "Tyler /Person/", "M")
        child2: Individual = Individual("m3", "Ricky /Person/", "M")
        child3: Individual = Individual("f2", "Sarah /Being/", "F")
        child4: Individual = Individual("m4", "Jack /Person/ Jr.", "M")
        family = Family("F1", husband.id, wife.id, [child1.id, child2.id, child3.id, child4.id])

        testReport.addToReport(husband)
        testReport.addToReport(wife)
        testReport.addToReport(child1)
        testReport.addToReport(child2)
        testReport.addToReport(child3)
        testReport.addToReport(family)

        testReport.check_family_male_surnames()
        self.assertEqual(len(testReport.errors), 0)
        

    def test_differing_male_surnames(self):
        testReport: Report = Report()
        husband: Individual = Individual("m1", "Jack /Person/", "M")
        wife: Individual = Individual("f1", "Mary /Human/", "F")
        child1: Individual = Individual("m2", "Tyler /Guy/", "M")
        child2: Individual = Individual("m3", "Ricky /Sapien/", "M")
        child3: Individual = Individual("f2", "Sarah /Being/", "F")
        family = Family("F1", husband.id, wife.id, [child1.id, child2.id, child3.id])

        testReport.addToReport(husband)
        testReport.addToReport(wife)
        testReport.addToReport(child1)
        testReport.addToReport(child2)
        testReport.addToReport(child3)
        testReport.addToReport(family)

        testReport.check_family_male_surnames()
        self.assertEqual(testReport.anomalies[0].detailType, "Differing Male Surnames")
        self.assertEqual(testReport.anomalies[0].message, "Males in family F1 have several different surnames ['Person', 'Guy', 'Sapien']")
