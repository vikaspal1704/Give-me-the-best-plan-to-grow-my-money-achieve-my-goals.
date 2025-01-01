import unittest
from database.db_operations import AstraDB
from langflow.insights_generator import InsightsGenerator

class TestSocialMediaAnalysis(unittest.TestCase):
    def setUp(self):
        self.db = AstraDB("secure-connect-database.zip")
        self.db.create_table()
        self.mock_data = [
            (1, 'carousel', 150, 20, 30),
            (2, 'reels', 300, 50, 100),
            (3, 'static', 100, 10, 20),
            (4, 'reels', 400, 70, 120),
            (5, 'carousel', 200, 30, 40)
        ]
        self.db.insert_data(self.mock_data)

    def test_query_data(self):
        metrics = self.db.query_data('carousel')
        self.assertIsNotNone(metrics)

    def test_insights_generation(self):
        metrics = self.db.query_data('reels')
        insights = InsightsGenerator.generate_insight(metrics)
        self.assertIsInstance(insights, str)
        self.assertIn("engagement", insights.lower())

if __name__ == "__main__":
    unittest.main()
