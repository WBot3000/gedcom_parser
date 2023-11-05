#US36 - List recent deaths 
import unittest
from datetime import datetime, date, timedelta
from your_module import GEDCOMParser  # Replace 'your_module' with the actual name of your module

class TestRecentDeaths(unittest.TestCase):
    def setUp(self):
        # Set up a GEDCOMParser instance for testing
        self.parser = GEDCOMParser()
        self.today = datetime.now().date()
        
    def test_recent_deaths_within_threshold(self):
        # Create individuals with death dates within the threshold
        recent_death1 = self.create_individual('I1', 'John Doe', 'M', self.today - timedelta(days=15))
        recent_death2 = self.create_individual('I2', 'Jane Smith', 'F', self.today - timedelta(days=10))
        recent_death3 = self.create_individual('I3', 'Tom Brown', 'M', self.today - timedelta(days=25))
        
        self.parser.individuals = {
            'I1': recent_death1,
            'I2': recent_death2,
            'I3': recent_death3,
        }
        
        recent_deaths = self.parser.list_recent_deaths(days_threshold=20)
        self.assertEqual(len(recent_deaths), 2)
        self.assertTrue(all(individual in recent_deaths for individual in [recent_death1, recent_death2]))
        
    def test_recent_deaths_outside_threshold(self):
        # Create individuals with death dates outside the threshold
        old_death1 = self.create_individual('I4', 'Old John', 'M', self.today - timedelta(days=60))
        old_death2 = self.create_individual('I5', 'Elderly Jane', 'F', self.today - timedelta(days=45))
        
        self.parser.individuals = {
            'I4': old_death1,
            'I5': old_death2,
        }
        
        recent_deaths = self.parser.list_recent_deaths(days_threshold=30)
        self.assertEqual(len(recent_deaths), 0)

    def create_individual(self, id, name, sex, death_date):
        individual = self.parser.create_individual(id)
        individual.name = name
        individual.sex = sex
        individual.death_date = death_date
        return individual

if __name__ == '__main__':
    unittest.main()
