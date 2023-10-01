import unittest

#Need this to import modules inside sibling directories
#current_directory = os.path.dirname(__file__)
#sibling_directory = os.path.join(current_directory, "..", "")
from classes.GEDCOM_Reporting import Report, ReportDetail
from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family

class US22_Tests(unittest.TestCase):
    def test_no_duplicates(self):
        testReport: Report = Report()
        idA = testReport.generateId("a")
        idB = testReport.generateId("b")
        idC = testReport.generateId("c")
        indiA: Individual = Individual(idA)
        indiB: Individual = Individual(idB)
        indiC: Individual = Individual(idC)
        testReport.addToMap(indiA)
        testReport.addToMap(indiB)
        testReport.addToMap(indiC)
        self.assertEqual(testReport.errors, [], "Test Report has errors, despite all IDs being unique")


    def test_single_duplicate(self):
        testReport: Report = Report()
        idA1 = testReport.generateId("a")
        indiA1: Individual = Individual(idA1)
        testReport.addToMap(indiA1)

        idA2 = testReport.generateId("a")
        indiA2: Individual = Individual(idA2)
        testReport.addToMap(indiA2)

        idC = testReport.generateId("c")
        indiC: Individual = Individual(idC)
        testReport.addToMap(indiC)

        self.assertEqual(testReport.errors, [ReportDetail("Duplicate IDs", "a is already used")], "Error details are incorrect, there should be mention of duplicate a's")
        self.assertEqual(idA2, "a (1)", "New ID for A2 not created correctly")


    def test_multiple_duplicates(self):
        testReport: Report = Report()
        idA1 = testReport.generateId("a")
        indiA1: Individual = Individual(idA1)
        testReport.addToMap(indiA1)

        idA2 = testReport.generateId("a")
        indiA2: Individual = Individual(idA2)
        testReport.addToMap(indiA2)

        idA3 = testReport.generateId("a")
        indiA3: Individual = Individual(idA3)
        testReport.addToMap(indiA3)

        self.assertEqual(testReport.errors, [ReportDetail("Duplicate IDs", "a is already used"), ReportDetail("Duplicate IDs", "a is already used")], "Error details are incorrect, there should be mention of duplicate a's")
        self.assertEqual(idA2, "a (1)", "New ID for A2 not created correctly")
        self.assertEqual(idA3, "a (2)", "New ID for A3 not created correctly")


    def test_indi_and_fam_duplicate(self):
        testReport: Report = Report()
        idIndi = testReport.generateId("a")
        indiA: Individual = Individual(idIndi)
        testReport.addToMap(indiA)

        idFam = testReport.generateId("a")
        famA: Family = Family(idFam)
        testReport.addToMap(famA)

        self.assertEqual(testReport.errors, [ReportDetail("Duplicate IDs", "a is already used")], "Error details are incorrect, there should be mention of duplicate a's")
        self.assertEqual(idFam, "a (1)", "New ID for famA not created correctly")

    
    #While generateId should always be used to create a new ID for a report, this failsafe should be useful
    def test_ignoring_generateId(self):
        testReport: Report = Report()
        indiA1: Individual = Individual("a")
        testReport.addToMap(indiA1)

        indiA2: Individual = Individual("a")
        testReport.addToMap(indiA2)

        indiC: Individual = Individual("c")
        testReport.addToMap(indiC)

        self.assertEqual(testReport.errors, [ReportDetail("Duplicate IDs", "a is already used")], "Error details are incorrect, there should be mention of duplicate a's")
        self.assertEqual(indiA2.id, "a (1)", "New ID for A2 not created correctly")