import unittest
from datetime import date
from classes.GEDCOM_Reporting import Report, ReportDetail

class US42_Tests(unittest.TestCase):
    def test_no_invalid_dates(self):
        testReport: Report = Report()
        testDate: date = testReport.getDateFromString("28 NOV 2001")
        self.assertEqual(testDate, date(2001, 11, 28))
        self.assertEqual(testReport.errors, [], "Test Report has errors, despite the generated date being valid")


    def test_invalid_year(self):
        testReport: Report = Report()
        testDate: date = testReport.getDateFromString("28 NOV BADYEAR")
        self.assertIsNone(testDate, "Date should be none due to invalid year")
        self.assertEqual(testReport.errors, [ReportDetail("Invalid Date", "<year> of date (BADYEAR) is not a valid numerical value")], "Error details are incorrect, there should be mention of an invalid year")


    def test_invalid_month(self):
        testReport: Report = Report()
        testDate: date = testReport.getDateFromString("28 BADMONTH 2001")
        self.assertIsNone(testDate, "Date should be none due to invalid month")
        self.assertEqual(testReport.errors, [ReportDetail("Invalid Date", "<month> of date (BADMONTH) is not a valid month string")], "Error details are incorrect, there should be mention of an invalid month")


    def test_invalid_day(self):
        testReport: Report = Report()
        testDate: date = testReport.getDateFromString("BADDAY NOV 2001")
        self.assertIsNone(testDate, "Date should be none due to invalid day")
        self.assertEqual(testReport.errors, [ReportDetail("Invalid Date", "<day> of date (BADDAY) is not a valid numerical value")], "Error details are incorrect, there should be mention of an invalid day")

    
    #All fields work individualy, but don't form a valid date together
    def test_impossible_date(self):
        testReport: Report = Report()
        testDate: date = testReport.getDateFromString("30 FEB 2001")
        self.assertIsNone(testDate, "Date should be none due to being impossible")
        self.assertEqual(testReport.errors, [ReportDetail("Invalid Date", "30 FEB 2001 is not a valid date (the day is probably too large for the current month)")], "Error details are incorrect, there should be mention of the day being too large for the month")