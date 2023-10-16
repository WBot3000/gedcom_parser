import unittest
from classes.GEDCOM_Reporting import Report, ReportDetail
from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family

class US22_Tests(unittest.TestCase):
    def test_no_duplicates(self):
        testReport: Report = Report()
        idA = testReport.check_unique_id_and_fix("a")
        idB = testReport.check_unique_id_and_fix("b")
        idC = testReport.check_unique_id_and_fix("c")
        indiA: Individual = Individual(idA)
        indiB: Individual = Individual(idB)
        indiC: Individual = Individual(idC)
        testReport.addToReport(indiA)
        testReport.addToReport(indiB)
        testReport.addToReport(indiC)
        self.assertEqual(testReport.errors, [], "Test Report has errors, despite all IDs being unique")


    def test_single_duplicate(self):
        testReport: Report = Report()
        idA1 = testReport.check_unique_id_and_fix("a")
        indiA1: Individual = Individual(idA1)
        testReport.addToReport(indiA1)

        idA2 = testReport.check_unique_id_and_fix("a")
        indiA2: Individual = Individual(idA2)
        testReport.addToReport(indiA2)

        idC = testReport.check_unique_id_and_fix("c")
        indiC: Individual = Individual(idC)
        testReport.addToReport(indiC)

        self.assertEqual(testReport.errors, [ReportDetail("Duplicate IDs", "a is already used")], "Error details are incorrect, there should be mention of duplicate a's")
        self.assertEqual(idA2, "a (1)", "New ID for A2 not created correctly")


    def test_multiple_duplicates(self):
        testReport: Report = Report()
        idA1 = testReport.check_unique_id_and_fix("a")
        indiA1: Individual = Individual(idA1)
        testReport.addToReport(indiA1)

        idA2 = testReport.check_unique_id_and_fix("a")
        indiA2: Individual = Individual(idA2)
        testReport.addToReport(indiA2)

        idA3 = testReport.check_unique_id_and_fix("a")
        indiA3: Individual = Individual(idA3)
        testReport.addToReport(indiA3)

        self.assertEqual(testReport.errors, [ReportDetail("Duplicate IDs", "a is already used"), ReportDetail("Duplicate IDs", "a is already used")], "Error details are incorrect, there should be mention of duplicate a's")
        self.assertEqual(idA2, "a (1)", "New ID for A2 not created correctly")
        self.assertEqual(idA3, "a (2)", "New ID for A3 not created correctly")


    def test_indi_and_fam_duplicate(self):
        testReport: Report = Report()
        idIndi = testReport.check_unique_id_and_fix("a")
        indiA: Individual = Individual(idIndi)
        testReport.addToReport(indiA)

        idFam = testReport.check_unique_id_and_fix("a")
        famA: Family = Family(idFam)
        testReport.addToReport(famA)

        self.assertEqual(testReport.errors, [ReportDetail("Duplicate IDs", "a is already used")], "Error details are incorrect, there should be mention of duplicate a's")
        self.assertEqual(idFam, "a (1)", "New ID for famA not created correctly")

    
    #While check_unique_id_and_fix should always be used to create a new ID for a report, this failsafe should be useful
    def test_ignoring_check_unique_id_and_fix(self):
        testReport: Report = Report()
        indiA1: Individual = Individual("a")
        testReport.addToReport(indiA1)

        indiA2: Individual = Individual("a")
        testReport.addToReport(indiA2)

        indiC: Individual = Individual("c")
        testReport.addToReport(indiC)

        self.assertEqual(testReport.errors, [ReportDetail("Duplicate IDs", "a is already used")], "Error details are incorrect, there should be mention of duplicate a's")
        self.assertEqual(indiA2.id, "a (1)", "New ID for A2 not created correctly")