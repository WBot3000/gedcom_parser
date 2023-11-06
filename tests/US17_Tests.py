import unittest
from classes.GEDCOM_Reporting import Report, ReportDetail
from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family

class TestNoMarriageToDescendants(unittest.TestCase):
    def test_no_marriage_to_descendants_no_issues(self):
        testReport: Report = Report()
        i1 = Individual("I1", "John Doe", "M", None, None, None, ["F1"])
        i2 = Individual("I2", "Jane Smith", "F", None, None, None, ["F1"])
        i3 = Individual("I3", "Child 1", "F", None, None, "F1", None)

        f1 = Family("F1", "I1", "I2", ["I3"], None, None)

        testReport.addToReport(i1)
        testReport.addToReport(i2)
        testReport.addToReport(i3)
        testReport.addToReport(f1)

        testReport.no_marriage_to_descendants()

        # Assert that there are no descendant marriages
        self.assertEqual(len(testReport.anomalies), 0)


    def test_marriage_to_descendant(self):
        testReport: Report = Report()
        i1 = Individual("I1", "John Doe", "M", None, None, None, ["F1"])
        i2 = Individual("I2", "Jane Smith", "F", None, None, None, None)
        i3 = Individual("I3", "Child 1", "F", None, None, "F1", ["F1"])

        f1 = Family("F1", "I1", "I3", ["I3"], None, None)

        testReport.addToReport(i1)
        testReport.addToReport(i2)
        testReport.addToReport(i3)
        testReport.addToReport(f1)

        testReport.no_marriage_to_descendants()

        # Assert that there are no descendant marriages
        self.assertEqual(len(testReport.anomalies), 1)
        self.assertEqual(testReport.anomalies[0].detailType, "Marriage to Descendant")
        self.assertEqual(testReport.anomalies[0].message, "I1 is married to descendant, I3.")