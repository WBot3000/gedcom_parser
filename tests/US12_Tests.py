import unittest
from datetime import date, datetime
from classes.GEDCOM_Reporting import Report, ReportDetail
from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family

class US12_Tests(unittest.TestCase):
    def test_parents_young_enough(self):
        testReport: Report = Report()
        dad = Individual ("I1", "Dad", "M", date(1972, 5, 1))
        mom = Individual ("I2", "Mom", "F", date(1973, 8, 28))
        child = Individual("I3", "Child", "F", date(2005, 12, 15))
        family = Family ("F1", dad.id, mom.id, [child.id])

        testReport.addToReport(dad)
        testReport.addToReport(mom)
        testReport.addToReport(child)
        testReport.addToReport(family)

        testReport.check_parent_child_age_difference()
        self.assertEqual(len(testReport.anomalies), 0)


    def test_mom_too_old(self):
        testReport: Report = Report()
        dad = Individual ("I1", "Dad", "M", date(1972, 5, 1))
        mom = Individual ("I2", "Mom", "F", date(1940, 8, 28))
        child = Individual("I3", "Child", "F", date(2005, 12, 15))
        family = Family ("F1", dad.id, mom.id, [child.id])

        testReport.addToReport(dad)
        testReport.addToReport(mom)
        testReport.addToReport(child)
        testReport.addToReport(family)

        testReport.check_parent_child_age_difference()
        self.assertEqual(testReport.anomalies[0].detailType, "Parent Too Old")
        self.assertEqual(testReport.anomalies[0].message, "Mother in family F1 is over 60 years older than one or more of her children ['I3']")


    def test_dad_too_old(self):
        testReport: Report = Report()
        dad = Individual ("I1", "Dad", "M", date(1920, 5, 1))
        mom = Individual ("I2", "Mom", "F", date(1973, 8, 28))
        child = Individual("I3", "Child", "F", date(2005, 12, 15))
        family = Family ("F1", dad.id, mom.id, [child.id])

        testReport.addToReport(dad)
        testReport.addToReport(mom)
        testReport.addToReport(child)
        testReport.addToReport(family)

        testReport.check_parent_child_age_difference()
        self.assertEqual(testReport.anomalies[0].detailType, "Parent Too Old")
        self.assertEqual(testReport.anomalies[0].message, "Father in family F1 is over 80 years older than one or more of his children ['I3']")


    def test_both_too_old(self):
        testReport: Report = Report()
        dad = Individual ("I1", "Dad", "M", date(1920, 5, 1))
        mom = Individual ("I2", "Mom", "F", date(1940, 8, 28))
        child = Individual("I3", "Child", "F", date(2005, 12, 15))
        family = Family ("F1", dad.id, mom.id, [child.id])

        testReport.addToReport(dad)
        testReport.addToReport(mom)
        testReport.addToReport(child)
        testReport.addToReport(family)

        testReport.check_parent_child_age_difference()
        self.assertEqual(testReport.anomalies[0].detailType, "Parent Too Old")
        self.assertEqual(testReport.anomalies[0].message, "Father in family F1 is over 80 years older than one or more of his children ['I3']")
        self.assertEqual(testReport.anomalies[1].detailType, "Parent Too Old")
        self.assertEqual(testReport.anomalies[1].message, "Mother in family F1 is over 60 years older than one or more of her children ['I3']")

    
    def test_mom_too_old_multiple_children(self):
        testReport: Report = Report()
        dad = Individual ("I1", "Dad", "M", date(1972, 5, 1))
        mom = Individual ("I2", "Mom", "F", date(1940, 8, 28))
        child1 = Individual("I3", "Child", "F", date(2005, 12, 15))
        child2 = Individual("I4", "Child", "M", date(2007, 9, 15))
        child3 = Individual("I5", "Child", "M", date(1990, 3, 7))
        family = Family ("F1", dad.id, mom.id, [child1.id, child2.id, child3.id])

        testReport.addToReport(dad)
        testReport.addToReport(mom)
        testReport.addToReport(child1)
        testReport.addToReport(child2)
        testReport.addToReport(child3)
        testReport.addToReport(family)

        testReport.check_parent_child_age_difference()
        self.assertEqual(testReport.anomalies[0].detailType, "Parent Too Old")
        self.assertEqual(testReport.anomalies[0].message, "Mother in family F1 is over 60 years older than one or more of her children ['I3', 'I4']")