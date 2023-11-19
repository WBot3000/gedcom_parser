#US38 - List upcoming birthdays
import unittest
from datetime import datetime, date
from classes.GEDCOM_Reporting import Report
from classes.GEDCOM_Units import Individual, Family


class TestUpcomingBirthdaysSorting(unittest.TestCase):

    def test_upcoming_birthdays_sorting(self):
        # Create a Report instance
        report = Report()

        # Create individuals with birthdays on various dates
        person1_birthday = datetime.today().date() + timedelta(days=3)
        person2_birthday = datetime.today().date() + timedelta(days=1)
        person3_birthday = datetime.today().date() + timedelta(days=7)
        person4_birthday = datetime.today().date() + timedelta(days=5)

        person1 = self.create_individual('Person1', person1_birthday)
        person2 = self.create_individual('Person2', person2_birthday)
        person3 = self.create_individual('Person3', person3_birthday)
        person4 = self.create_individual('Person4', person4_birthday)

        # Add individuals to the report
        report.indi_map = {
            'Person1': person1,
            'Person2': person2,
            'Person3': person3,
            'Person4': person4,
        }

        # Call the function to update recent births within the report
        report.list_recent_births(days_threshold=20)

        # Test if the system correctly sorts upcoming birthdays in chronological order
        people_data = [
            ("Person1", person1_birthday),
            ("Person2", person2_birthday),
            ("Person3", person3_birthday),
            ("Person4", person4_birthday),
        ]
        


    def test_upcoming_birthdays_empty_list(self):
        # Test when the list of upcoming birthdays is empty
        people_data = []
        upcoming_birthdays_list = upcoming_birthdays(people_data, days=7)
        self.assertEqual(upcoming_birthdays_list, [])

    def test_upcoming_birthdays_single_person(self):
        # Test when there's only one person with a birthday
        person_birthday = datetime.today().date() + timedelta(days=3)
        person = self.create_individual('Person', person_birthday)
        report = Report()
        report.indi_map = {'Person': person}
        upcoming_birthdays_list = upcoming_birthdays([(person.id, person_birthday)], days=7)
        self.assertEqual(upcoming_birthdays_list, [(person.id, person_birthday)])

    def test_upcoming_birthdays_same_day(self):
        # Test when multiple people have birthdays on the same day
        common_birthday = datetime.today().date() + timedelta(days=5)
        person1 = self.create_individual('Person1', common_birthday)
        person2 = self.create_individual('Person2', common_birthday)
        report = Report()
        report.indi_map = {'Person1': person1, 'Person2': person2}
        upcoming_birthdays_list = upcoming_birthdays([(person1.id, common_birthday), (person2.id, common_birthday)], days=7)
        self.assertEqual(upcoming_birthdays_list, [(person1.id, common_birthday), (person2.id, common_birthday)])

        upcoming_birthdays_list = upcoming_birthdays(people_data, days=7)

        # Sort the expected output to compare with the actual output
        expected_sorted_birthdays = sorted(people_data, key=lambda x: x[1])

        # Extract the names from the sorted expected output
        expected_sorted_names = [person[0] for person in expected_sorted_birthdays]

        # Extract the names from the actual output
        actual_names = [person for person, _ in upcoming_birthdays_list]

        self.assertEqual(actual_names, expected_sorted_names)

        def create_individual(self, id, name, sex, birth_date):
            return Individual(id, name, sex, birth_date, None, None, [])


if __name__ == '__main__':
    unittest.main()
