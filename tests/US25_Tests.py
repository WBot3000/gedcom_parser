import unittest
from classes.GEDCOM_Reporting import Report
from classes.GEDCOM_Units import Individual, Family
from datetime import date

class US25_Tests(unittest.TestCase):
    def test_no_entities(self):
        testReport = Report()
        testReport.check_sibling_same_name()
        self.assertEqual(len(testReport.anomalies), 0)


    def test_no_similarities(self):
        testReport = Report()
        I1 = Individual("I1", "Carl /Johnson/", "M", date(1990, 4, 3))
        I2 = Individual("I2", "Jack /Johnson/", "M", date(1992, 8, 9))
        I3 = Individual("I3", "Sarah /Johnson/", "F", date(1997, 5, 4))
        F1 = Family("F1", None, None, ["I1", "I2", "I3"], None, None)

        testReport.addToReport(I1)
        testReport.addToReport(I2)
        testReport.addToReport(I3)
        testReport.addToReport(F1)
        testReport.check_sibling_same_name()
        self.assertEqual(len(testReport.anomalies), 0)


    def test_one_similarity(self):
        testReport = Report()
        I1 = Individual("I1", "Carl /Johnson/", "M", date(1990, 4, 3))
        I2 = Individual("I2", "Carl /Johnson/", "M", date(1990, 4, 3))
        I3 = Individual("I3", "Sarah /Johnson/", "F", date(1997, 5, 4))
        F1 = Family("F1", None, None, ["I1", "I2", "I3"], None, None)

        testReport.addToReport(I1)
        testReport.addToReport(I2)
        testReport.addToReport(I3)
        testReport.addToReport(F1)
        testReport.check_sibling_same_name()
        self.assertEqual(len(testReport.anomalies), 1)
        self.assertEqual(testReport.anomalies[0].detailType, "Siblings Shared Name")
        self.assertEqual(testReport.anomalies[0].message, "Siblings ['I1', 'I2'] share a first name (Carl)")

    def test_one_similarity_multiple_siblings(self):
        testReport = Report()
        I1 = Individual("I1", "Carl /Johnson/", "M", date(1990, 4, 3))
        I2 = Individual("I2", "Carl /Johnson/", "M", date(1990, 4, 3))
        I3 = Individual("I3", "Carl /Johnson/", "F", date(1990, 4, 3))
        F1 = Family("F1", None, None, ["I1", "I2", "I3"], None, None)

        testReport.addToReport(I1)
        testReport.addToReport(I2)
        testReport.addToReport(I3)
        testReport.addToReport(F1)
        testReport.check_sibling_same_name()
        self.assertEqual(len(testReport.anomalies), 1)
        self.assertEqual(testReport.anomalies[0].detailType, "Siblings Shared Name")
        self.assertEqual(testReport.anomalies[0].message, "Siblings ['I1', 'I2', 'I3'] share a first name (Carl)")


    def test_different_similarities(self):
        testReport = Report()
        I1 = Individual("I1", "Carl /Johnson/", "M", date(1990, 4, 3))
        I2 = Individual("I2", "Carl /Johnson/", "M", date(1990, 4, 3))
        I3 = Individual("I3", "Sarah /Johnson/", "F", date(1997, 5, 4))
        I4 = Individual("I4", "Sarah /Johnson/", "F", date(1997, 5, 4))
        F1 = Family("F1", None, None, ["I1", "I2", "I3", "I4"], None, None)

        testReport.addToReport(I1)
        testReport.addToReport(I2)
        testReport.addToReport(I3)
        testReport.addToReport(I4)
        testReport.addToReport(F1)
        testReport.check_sibling_same_name()
        self.assertEqual(len(testReport.anomalies), 2)
        self.assertEqual(testReport.anomalies[0].detailType, "Siblings Shared Name")
        self.assertEqual(testReport.anomalies[0].message, "Siblings ['I1', 'I2'] share a first name (Carl)")
        self.assertEqual(testReport.anomalies[1].detailType, "Siblings Shared Name")
        self.assertEqual(testReport.anomalies[1].message, "Siblings ['I3', 'I4'] share a first name (Sarah)")