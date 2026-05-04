import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from leaderboard import Leaderboard


class TestLeaderboard(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_leaderboard.json"
        self.leaderboard = Leaderboard(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_score(self):
        self.leaderboard.add_score("AAA", 100)
        scores = self.leaderboard.get_top()
        self.assertEqual(len(scores), 1)
        self.assertEqual(scores[0]['name'], "AAA")

    def test_top_scores_sorted(self):
        self.leaderboard.add_score("AAA", 100)
        self.leaderboard.add_score("BBB", 200)
        scores = self.leaderboard.get_top()
        self.assertEqual(scores[0]['score'], 200)

    def test_is_high_score_empty(self):
        self.assertTrue(self.leaderboard.is_high_score(100))

    def test_max_scores(self):
        for i in range(15):
            self.leaderboard.add_score(f"P{i}", i * 100)
        scores = self.leaderboard.get_top()
        self.assertLessEqual(len(scores), 10)


if __name__ == "__main__":
    unittest.main()