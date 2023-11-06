import unittest
from datetime import date
from classes.GEDCOM_Reporting import Report
from classes.GEDCOM_Units import Individual, Family

class US19_Tests(unittest.TestCase):
    def test_first_cousins_marrying(self):
        # Create a report instance
        testReport = Report()

        # Create individuals
        grandpa = Individual("G1", "Grandpa Doe", "M", None, None, None, ["F1"])
        grandma = Individual("G2", "Grandma Doe", "F", None, None, None, ["F1"])
        john = Individual("I1", "John Doe", "M", None, None, "F1", ["F2"])
        mary = Individual("I2", "Mary Smith", "F", None, None, None, ["F2"])
        alice = Individual("I3", "Alice Doe", "F", None, None, "F2", ["F4"])
        mike = Individual("I4", "Mike Doe", "M", None, None, "F1", ["F3"])
        june = Individual("I5", "June Mae", "F", None, None, None, ["F3"])
        tyler = Individual("I6", "Tyler Doe", "M", None, None, "F3", ["F4"])

        # Create families
        family1 = Family("F1", grandpa.id, grandma.id, [john.id, mike.id], None, None)
        family2 = Family("F2", john.id, mary.id, [alice.id], None, None)
        family3 = Family("F3", mike.id, june.id, [tyler.id], None, None)
        family4 = Family("F4", tyler.id, alice.id, [], None, None)

        # Add individuals and families to the report
        testReport.addToReport(grandpa)
        testReport.addToReport(grandma)
        testReport.addToReport(john)
        testReport.addToReport(mary)
        testReport.addToReport(alice)
        testReport.addToReport(mike)
        testReport.addToReport(june)
        testReport.addToReport(tyler)

        testReport.addToReport(family1)
        testReport.addToReport(family2)
        testReport.addToReport(family3)
        testReport.addToReport(family4)

        # Call the function to check for first cousins marrying
        testReport.first_cousins_should_not_marry()

        # Assert that there is an error in the report
        self.assertEqual(len(testReport.anomalies), 1)
        self.assertEqual(testReport.anomalies[0].detailType, "First Cousins Marrying")
        self.assertEqual(testReport.anomalies[0].message, "First cousins are getting married in Family F4")

    def test_no_first_cousins_marrying(self):
        # Create a report instance
        testReport = Report()

        # Create individuals
        grandpa = Individual("G1", "Grandpa Doe", "M", None, None, None, ["F1"])
        grandma = Individual("G2", "Grandma Doe", "F", None, None, None, ["F1"])
        john = Individual("I1", "John Doe", "M", None, None, "F1", ["F2"])
        mary = Individual("I2", "Mary Smith", "F", None, None, None, ["F2"])
        alice = Individual("I3", "Alice Doe", "F", None, None, "F2", ["F4"])
        mike = Individual("I4", "Mike Doe", "M", None, None, "F1", ["F3"])
        june = Individual("I5", "June Mae", "F", None, None, None, ["F3"])
        tyler = Individual("I6", "Tyler Doe", "M", None, None, None, ["F4"])

        # Create families
        family1 = Family("F1", grandpa.id, grandma.id, [john.id, mike.id], None, None)
        family2 = Family("F2", john.id, mary.id, [alice.id], None, None)
        family3 = Family("F3", mike.id, june.id, [], None, None)
        family4 = Family("F4", tyler.id, alice.id, [], None, None)

        # Add individuals and families to the report
        testReport.addToReport(grandpa)
        testReport.addToReport(grandma)
        testReport.addToReport(john)
        testReport.addToReport(mary)
        testReport.addToReport(alice)
        testReport.addToReport(mike)
        testReport.addToReport(june)
        testReport.addToReport(tyler)

        testReport.addToReport(family1)
        testReport.addToReport(family2)
        testReport.addToReport(family3)
        testReport.addToReport(family4)

        # Call the function to check for first cousins marrying
        testReport.first_cousins_should_not_marry()

        # Assert that there is an error in the report
        self.assertEqual(len(testReport.anomalies), 0)
