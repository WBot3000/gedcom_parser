#US21
import unittest
from datetime import datetime, date
from classes.GEDCOM_Units import GEDCOMUnit, Individual, Family
from classes.GEDCOM_Reporting import Report

class TestCheckCorrectGenderForRoles(unittest.TestCase):
    def test_correct_gender_for_husband_and_wife(self):
        # Create a GedcomParser instance
        parser = GEDCOMUnit()

        # Create individuals
        husband = Individual("Husband", "Husband /Lastname/", "M", date(1980, 1, 1), None, None, None)
        wife = Individual("Wife", "Wife /Lastname/", "F", date(1985, 2, 2), None, None, None)

        # Create a family with a correct husband and wife
        family = Family("F1", husband.id, wife.id, [], None, None)

        # Add individuals and family to the parser
        parser.indi_map[husband.id] = husband
        parser.indi_map[wife.id] = wife
        parser.fam_map[family.id] = family

        # Run the check_correct_gender_for_roles method
        parser.check_correct_gender_for_roles()

        # Assert that there are no errors in the report
        self.assertEqual(len(parser.errors), 0)

    def test_incorrect_gender_for_husband(self):
        # Create a GedcomParser instance
        parser = GEDCOMUnit()

        # Create individuals with incorrect genders
        husband = Individual("Husband", "Husband /Lastname/", "F", date(1980, 1, 1), None, None, None)
        wife = Individual("Wife", "Wife /Lastname/", "F", date(1985, 2, 2), None, None, None)

        # Create a family with an incorrect husband gender
        family = Family("F1", husband.id, wife.id, [], None, None)

        # Add individuals and family to the parser
        parser.indi_map[husband.id] = husband
        parser.indi_map[wife.id] = wife
        parser.fam_map[family.id] = family

        # Run the check_correct_gender_for_roles method
        parser.check_correct_gender_for_roles()

        # Assert that there is an error in the report
        self.assertEqual(len(parser.errors), 1)
        self.assertEqual(parser.errors[0].message, "Husband in family F1 is female")

    def test_incorrect_gender_for_wife(self):
        # Create a GedcomParser instance
        parser = GEDCOMUnit()

        # Create individuals with incorrect genders
        husband = Individual("Husband", "Husband /Lastname/", "M", date(1980, 1, 1), None, None, None)
        wife = Individual("Wife", "Wife /Lastname/", "M", date(1985, 2, 2), None, None, None)

        # Create a family with an incorrect wife gender
        family = Family("F1", husband.id, wife.id, [], None, None)

        # Add individuals and family to the parser
        parser.indi_map[husband.id] = husband
        parser.indi_map[wife.id] = wife
        parser.fam_map[family.id] = family

        # Run the check_correct_gender_for_roles method
        parser.check_correct_gender_for_roles()

        # Assert that there is an error in the report
        self.assertEqual(len(parser.errors), 1)
        self.assertEqual(parser.errors[0].message, "Wife in family F1 is male")
