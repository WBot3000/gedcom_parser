import unittest
from datetime import date, datetime
from classes.GEDCOM_Reporting import Report, ReportDetail
from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family

class US01_Tests(unittest.TestCase):
    def test_past_dates(self):
        testReport: Report = Report()
        pastDate: date = date(2000, 1, 1)
        testReport.check_for_future_dates(pastDate)
        self.assertEqual(testReport.errors, [], "Test Report has errors, despite all dates being in the past")


    def test_today_date(self):
        testReport: Report = Report()
        todayDate: date = datetime.today().date()
        testReport.check_for_future_dates(todayDate)
        self.assertEqual(testReport.errors, [], "Test Report has errors, despite today's date being valid for entry")


    def test_future_dates(self):
        testReport: Report = Report()
        futureDate: date = date(2099, 1, 1)
        testReport.check_for_future_dates(futureDate)
        self.assertEqual(testReport.errors, [ReportDetail("Future Date", "Date that has yet to happen (2099-01-01) has been detected")])


    def test_no_date(self):
        testReport: Report = Report()
        testReport.check_for_future_dates(None)
        self.assertEqual(testReport.errors, [], "Test Report has errors, None should be skipped over while checking for future dates")