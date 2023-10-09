import unittest
from datetime import datetime, date
from classes.GEDCOM_Reporting import Report
from classes.GEDCOM_Units import Individual, Family

class US28_Tests(unittest.TestCase):
    def test_no_children (self):
        testReport: Report = Report()
        family = Family ("F1")
        testReport.addToReport(family)
        testReport.sort_children_by_age()
        self.assertEqual(len(family.childIds), 0)


    def test_single_child (self):
        testReport: Report = Report()
        family = Family ("F1", None, None, ["onlychild"], None, None)
        child = Individual ("onlychild", "Only /Child/", "F", date(2000, 8, 7), None, "F1", None)
        testReport.addToReport(family)
        testReport.addToReport(child)
        testReport.sort_children_by_age()
        self.assertEqual(family.childIds, ["onlychild"])


    def test_two_children (self):
        testReport: Report = Report()
        family = Family ("F1", None, None, ["youngest", "oldest"], None, None)
        youngest = Individual ("youngest", "Youngest /Child/", "F", date(2007, 2, 3), None, "F1", None)
        oldest = Individual ("oldest", "Oldest /Child/", "F", date(2000, 5, 5), None, "F1", None)
        testReport.addToReport(family)
        testReport.addToReport(youngest)
        testReport.addToReport(oldest)
        testReport.sort_children_by_age()
        self.assertEqual(family.childIds, ["oldest", "youngest"])

    def test_twins (self):
        testReport: Report = Report()
        family = Family ("F1", None, None, ["twinA", "twinB"], None, None)
        twinA = Individual ("twinA", "A /Twin/", "F", date(2004, 4, 28), None, "F1", None)
        twinB = Individual ("twinB", "B /Twin/", "F", date(2004, 4, 28), None, "F1", None)
        testReport.addToReport(family)
        testReport.addToReport(twinA)
        testReport.addToReport(twinB)
        testReport.sort_children_by_age()
        self.assertEqual(family.childIds, ["twinA", "twinB"])


    def test_three_children (self):
        testReport: Report = Report()
        family = Family ("F1", None, None, ["youngest", "oldest", "middle"], None, None)
        youngest = Individual ("youngest", "Youngest /Child/", "F", date(2007, 2, 3), None, "F1", None)
        oldest = Individual ("oldest", "Oldest /Child/", "F", date(2000, 5, 5), None, "F1", None)
        middle = Individual ("middle", "Middle /Child/", "F", date(2003, 9, 9), None, "F1", None)
        testReport.addToReport(family)
        testReport.addToReport(youngest)
        testReport.addToReport(oldest)
        testReport.addToReport(middle)
        testReport.sort_children_by_age()
        self.assertEqual(family.childIds, ["oldest", "middle", "youngest"])

    
    def test_twins_plus_other (self):
        testReport: Report = Report()
        family = Family ("F1", None, None, ["twinA", "twinB", "oldest"], None, None)
        twinA = Individual ("twinA", "A /Twin/", "F", date(2004, 4, 28), None, "F1", None)
        twinB = Individual ("twinB", "B /Twin/", "F", date(2004, 4, 28), None, "F1", None)
        oldest = Individual ("oldest", "Oldest /Child/", "F", date(2000, 5, 5), None, "F1", None)
        testReport.addToReport(family)
        testReport.addToReport(twinA)
        testReport.addToReport(twinB)
        testReport.addToReport(oldest)
        testReport.sort_children_by_age()
        self.assertEqual(family.childIds, ["oldest", "twinA", "twinB"])

    
    def test_four_children (self):
        testReport: Report = Report()
        family = Family ("F1", None, None, ["second", "youngest", "oldest", "third"], None, None)
        youngest = Individual ("youngest", "Youngest /Child/", "F", date(2007, 2, 3), None, "F1", None)
        oldest = Individual ("oldest", "Oldest /Child/", "F", date(2000, 5, 5), None, "F1", None)
        second = Individual ("second", "Second /Child/", "F", date(2003, 9, 9), None, "F1", None)
        third = Individual ("third", "Second /Child/", "F", date(2005, 6, 12), None, "F1", None)
        testReport.addToReport(family)
        testReport.addToReport(youngest)
        testReport.addToReport(oldest)
        testReport.addToReport(second)
        testReport.addToReport(third)
        testReport.sort_children_by_age()
        self.assertEqual(family.childIds, ["oldest", "second", "third", "youngest"])


    def test_child_no_bdate (self):
        testReport: Report = Report()
        family = Family ("F1", None, None, ["youngest", "nobdate", "oldest"], None, None)
        youngest = Individual ("youngest", "Youngest /Child/", "F", date(2007, 2, 3), None, "F1", None)
        oldest = Individual ("oldest", "Oldest /Child/", "F", date(2000, 5, 5), None, "F1", None)
        nobdate = Individual ("nobdate", "No Birthday /Child/", "F", None, None, "F1", None)
        testReport.addToReport(family)
        testReport.addToReport(youngest)
        testReport.addToReport(oldest)
        testReport.addToReport(nobdate)
        testReport.sort_children_by_age()
        self.assertEqual(family.childIds, ["oldest", "youngest", "nobdate"])


    def test_just_born (self):
        testReport: Report = Report()
        family = Family ("F1", None, None, ["newborn", "oldest"], None, None)
        newborn = Individual ("newborn", "Newborn /Child/", "F", datetime.today().date(), None, "F1", None)
        oldest = Individual ("oldest", "Oldest /Child/", "F", date(2000, 5, 5), None, "F1", None)
        testReport.addToReport(family)
        testReport.addToReport(newborn)
        testReport.addToReport(oldest)
        testReport.sort_children_by_age()
        self.assertEqual(family.childIds, ["oldest", "newborn"])