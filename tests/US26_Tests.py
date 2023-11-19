import unittest
from classes.GEDCOM_Reporting import Report
from classes.GEDCOM_Units import Individual, Family

class US26_Tests(unittest.TestCase):
    def test_no_entries(self):
        testReport = Report()
        testReport.check_corresponding_entries()
        self.assertEqual(len(testReport.errors), 0)


    def test_all_corresponding_entries(self):
        testReport = Report()
        I1 = Individual("I1", "Husband", "M", None, None, None, ["F1"])
        I2 = Individual("I2", "Wife", "F", None, None, None, ["F1"])
        I3 = Individual("I3", "Child A", "M", None, None, "F1", None)
        I4 = Individual("I4", "Child B", "M", None, None, "F1", None)
        F1 = Family("F1", "I1", "I2", ["I3", "I4"], None, None)

        testReport.addToReport(I1)
        testReport.addToReport(I2)
        testReport.addToReport(I3)
        testReport.addToReport(I4)
        testReport.addToReport(F1)
        testReport.check_corresponding_entries()
        self.assertEqual(len(testReport.errors), 0)


    # Tests for entries that don't exist at all
    def test_missing_husband(self):
        testReport = Report()
        I2 = Individual("I2", "Wife", "F", None, None, None, ["F1"])
        I3 = Individual("I3", "Child A", "M", None, None, "F1", None)
        I4 = Individual("I4", "Child B", "M", None, None, "F1", None)
        F1 = Family("F1", "I1", "I2", ["I3", "I4"], None, None)

        testReport.addToReport(I2)
        testReport.addToReport(I3)
        testReport.addToReport(I4)
        testReport.addToReport(F1)
        testReport.check_corresponding_entries()
        self.assertEqual(len(testReport.errors), 1)
        self.assertEqual(testReport.errors[0].detailType, "Correspondance Error")
        self.assertEqual(testReport.errors[0].message, "Husband I1 specified in family F1 is not present in the individual records")


    def test_missing_husband(self):
        testReport = Report()
        I1 = Individual("I1", "Husband", "M", None, None, None, ["F1"])
        I3 = Individual("I3", "Child A", "M", None, None, "F1", None)
        I4 = Individual("I4", "Child B", "M", None, None, "F1", None)
        F1 = Family("F1", "I1", "I2", ["I3", "I4"], None, None)

        testReport.addToReport(I1)
        testReport.addToReport(I3)
        testReport.addToReport(I4)
        testReport.addToReport(F1)
        testReport.check_corresponding_entries()
        self.assertEqual(len(testReport.errors), 1)
        self.assertEqual(testReport.errors[0].detailType, "Correspondance Error")
        self.assertEqual(testReport.errors[0].message, "Wife I2 specified in family F1 is not present in the individual records")


    def test_missing_child(self):
        testReport = Report()
        I1 = Individual("I1", "Husband", "M", None, None, None, ["F1"])
        I2 = Individual("I2", "Wife", "F", None, None, None, ["F1"])
        I4 = Individual("I4", "Child B", "M", None, None, "F1", None)
        F1 = Family("F1", "I1", "I2", ["I3", "I4"], None, None)

        testReport.addToReport(I1)
        testReport.addToReport(I2)
        testReport.addToReport(I4)
        testReport.addToReport(F1)
        testReport.check_corresponding_entries()
        self.assertEqual(len(testReport.errors), 1)
        self.assertEqual(testReport.errors[0].detailType, "Correspondance Error")
        self.assertEqual(testReport.errors[0].message, "Child I3 specified in family F1 is not present in the individual records")


    def test_missing_family(self):
        testReport = Report()
        I1 = Individual("I1", "Husband", "M", None, None, None, ["F1"])
        I2 = Individual("I2", "Wife", "F", None, None, None, ["F1"])
        I3 = Individual("I3", "Child A", "M", None, None, "F1", None)
        I4 = Individual("I4", "Child B", "M", None, None, "F1", None)

        testReport.addToReport(I1)
        testReport.addToReport(I2)
        testReport.addToReport(I3)
        testReport.addToReport(I4)
        testReport.check_corresponding_entries()

        self.assertEqual(len(testReport.errors), 4)
        self.assertEqual(testReport.errors[0].detailType, "Correspondance Error")
        self.assertEqual(testReport.errors[0].message, "Family F1 specified in individual I1 is not present in the family records")
        self.assertEqual(testReport.errors[1].detailType, "Correspondance Error")
        self.assertEqual(testReport.errors[1].message, "Family F1 specified in individual I2 is not present in the family records")
        self.assertEqual(testReport.errors[2].detailType, "Correspondance Error")
        self.assertEqual(testReport.errors[2].message, "Family F1 specified in individual I3 is not present in the family records")
        self.assertEqual(testReport.errors[3].detailType, "Correspondance Error")
        self.assertEqual(testReport.errors[3].message, "Family F1 specified in individual I4 is not present in the family records")



    # Tests for situations where all the entires exist, but there's a mismatch somewhere
    def test_mismatched_husband(self):
        testReport = Report()
        I1 = Individual("I1", "Husband", "M", None, None, None, ["F1"])
        I2 = Individual("I2", "Wife", "F", None, None, None, ["F1"])
        I3 = Individual("I3", "Child A", "M", None, None, "F1", None)
        I4 = Individual("I4", "Child B", "M", None, None, "F1", None)
        F1 = Family("F1", None, "I2", ["I3", "I4"], None, None)
        F2 = Family("F2", "I1", None, [], None, None)

        testReport.addToReport(I1)
        testReport.addToReport(I2)
        testReport.addToReport(I3)
        testReport.addToReport(I4)
        testReport.addToReport(F1)
        testReport.addToReport(F2)
        testReport.check_corresponding_entries()
        self.assertEqual(len(testReport.errors), 2)
        self.assertEqual(testReport.errors[0].detailType, "Correspondance Error")
        self.assertEqual(testReport.errors[0].message, "Family F1 specified in individual I1 does not have I1 as a spouse")
        self.assertEqual(testReport.errors[1].detailType, "Correspondance Error")
        self.assertEqual(testReport.errors[1].message, "Husband I1 specified in family F2 does not have F2 as a corresponding spousal family")


    def test_mismatched_wife(self):
        testReport = Report()
        I1 = Individual("I1", "Husband", "M", None, None, None, ["F1"])
        I2 = Individual("I2", "Wife", "F", None, None, None, ["F1"])
        I3 = Individual("I3", "Child A", "M", None, None, "F1", None)
        I4 = Individual("I4", "Child B", "M", None, None, "F1", None)
        F1 = Family("F1", "I1", None, ["I3", "I4"], None, None)
        F2 = Family("F2", None, "I2", [], None, None)

        testReport.addToReport(I1)
        testReport.addToReport(I2)
        testReport.addToReport(I3)
        testReport.addToReport(I4)
        testReport.addToReport(F1)
        testReport.addToReport(F2)
        testReport.check_corresponding_entries()
        self.assertEqual(len(testReport.errors), 2)
        self.assertEqual(testReport.errors[0].detailType, "Correspondance Error")
        self.assertEqual(testReport.errors[0].message, "Family F1 specified in individual I2 does not have I2 as a spouse")
        self.assertEqual(testReport.errors[1].detailType, "Correspondance Error")
        self.assertEqual(testReport.errors[1].message, "Wife I2 specified in family F2 does not have F2 as a corresponding spousal family")


    def test_mismatched_child(self):
        testReport = Report()
        I1 = Individual("I1", "Husband", "M", None, None, None, ["F1"])
        I2 = Individual("I2", "Wife", "F", None, None, None, ["F1"])
        I3 = Individual("I3", "Child A", "M", None, None, "F1", None)
        I4 = Individual("I4", "Child B", "M", None, None, "F1", None)
        F1 = Family("F1", "I1", "I2", ["I4"], None, None)
        F2 = Family("F2", None, None, ["I3"], None, None)

        testReport.addToReport(I1)
        testReport.addToReport(I2)
        testReport.addToReport(I3)
        testReport.addToReport(I4)
        testReport.addToReport(F1)
        testReport.addToReport(F2)
        testReport.check_corresponding_entries()
        self.assertEqual(len(testReport.errors), 2)
        self.assertEqual(testReport.errors[0].detailType, "Correspondance Error")
        self.assertEqual(testReport.errors[0].message, "Family F1 specified in individual I3 does not have I3 as a child")
        self.assertEqual(testReport.errors[1].detailType, "Correspondance Error")
        self.assertEqual(testReport.errors[1].message, "Child I3 specified in family F2 does not have F2 as their childhood family")
        

