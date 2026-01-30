import sys
import os
import unittest

# Get the path to the project's root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from src import stats


class TestStats(unittest.TestCase):

    def test_calculate_mean(self):
        """Test mean calculation"""
        self.assertEqual(stats.calculate_mean([10, 20, 30, 40, 50]), 30.0)
        self.assertEqual(stats.calculate_mean([5, 15, 25]), 15.0)
        self.assertEqual(stats.calculate_mean([100]), 100.0)
        self.assertEqual(stats.calculate_mean([-5, 0, 5]), 0.0)
        self.assertEqual(stats.calculate_mean([7, 14, 21]), 14.0)

    def test_calculate_median(self):
        """Test median calculation"""
        self.assertEqual(stats.calculate_median([10, 20, 30, 40, 50]), 30)
        self.assertEqual(stats.calculate_median([5, 10, 15, 20]), 12.5)
        self.assertEqual(stats.calculate_median([42]), 42)
        self.assertEqual(stats.calculate_median([7, 3, 9]), 7)
        self.assertEqual(stats.calculate_median([100, 200, 300]), 200)

    def test_calculate_mode(self):
        """Test mode calculation"""
        self.assertEqual(stats.calculate_mode([5, 10, 10, 15, 20]), [10])
        self.assertEqual(stats.calculate_mode([3, 3, 7, 7, 9]), [3, 7])
        self.assertEqual(stats.calculate_mode([8, 8, 8, 2, 4]), [8])
        self.assertEqual(stats.calculate_mode([11, 22, 33, 44, 55]), [])
        self.assertEqual(stats.calculate_mode([6, 6, 6, 6]), [6])

    def test_calculate_variance(self):
        """Test variance calculation"""
        self.assertEqual(stats.calculate_variance([10, 20, 30, 40, 50]), 200.0)
        self.assertEqual(stats.calculate_variance([15, 15, 15]), 0.0)
        self.assertAlmostEqual(stats.calculate_variance([5, 10, 15, 20]), 31.25, places=2)
        self.assertEqual(stats.calculate_variance([7]), 0.0)

    def test_calculate_std_deviation(self):
        """Test standard deviation calculation"""
        self.assertAlmostEqual(stats.calculate_std_deviation([10, 20, 30, 40, 50]), 14.1421, places=4)
        self.assertEqual(stats.calculate_std_deviation([25, 25, 25]), 0.0)
        self.assertAlmostEqual(stats.calculate_std_deviation([5, 10, 15, 20]), 5.5902, places=4)
        self.assertEqual(stats.calculate_std_deviation([12]), 0.0)

    def test_empty_list_errors(self):
        """Test that empty lists raise ValueError"""
        with self.assertRaises(ValueError):
            stats.calculate_mean([])
        with self.assertRaises(ValueError):
            stats.calculate_median([])
        with self.assertRaises(ValueError):
            stats.calculate_mode([])

    def test_invalid_input_errors(self):
        """Test that non-numeric values raise ValueError"""
        with self.assertRaises(ValueError):
            stats.calculate_mean([10, 20, "thirty"])
        with self.assertRaises(ValueError):
            stats.calculate_median([5, None, 15])


if __name__ == '__main__':
    unittest.main()