#US18 - Siblings should not marry
import unittest
from classes.GEDCOM_Reporting import Report
from classes.GEDCOM_Units import Individual, Family

class TestNoSiblingMarriage(unittest.TestCase):
    def test_no_sibling_marriage_no_issues(self):
        # Scenario where there are no sibling marriages
        testInstance = Report()

        i1 = Individual("I1", "John Doe", "M", None, None, None, ["F1"])
        i2 = Individual("I2", "Jane Smith", "F", None, None, None, ["F1"])
        i3 = Individual("I3", "Child 1", "F", None, None, "F1", None)

        f1 = Family("F1", "I1", "I2", ["I3"], None, None)

        testInstance.indi_map = {"I1": i1, "I2": i2, "I3": i3}
        testInstance.fam_map = {"F1": f1}

        testInstance.no_sibling_marriage()

        # Assert that there are no sibling marriages
        self.assertEqual(len(testInstance.anomalies), 0)

    def test_sibling_marriage(self):
        # Scenario where there is a sibling marriage
        testInstance = Report()

        i1 = Individual("I1", "John Doe", "M", None, None, None, ["F1"])
        i2 = Individual("I2", "Jane Smith", "F", None, None, None, ["F1"])
        i3 = Individual("I3", "Child 1", "F", None, None, "F1", ["F2"])
        i4 = Individual("I4", "Child 2", "M", None, None, "F1", ["F2"])

        f1 = Family("F1", "I1", "I2", ["I3", "I4"], None, None)
        f2 = Family("F2", "I4", "I3", [], None, None)

        testInstance.indi_map = {"I1": i1, "I2": i2, "I3": i3, "I4": i4}
        testInstance.fam_map = {"F1": f1, "F2": f2}

        testInstance.no_sibling_marriage()

        # Assert that there is a sibling marriage anomaly
        self.assertEqual(len(testInstance.anomalies), 1)
        self.assertEqual(testInstance.anomalies[0].detailType, "Sibling Marriage")
        self.assertEqual(testInstance.anomalies[0].message, "Siblings I4 and I3 should not marry.")

    # Add more test cases as needed

if __name__ == '__main__':
    unittest.main()
