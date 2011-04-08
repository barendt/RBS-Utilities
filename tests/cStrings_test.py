#!/usr/bin/env python

import unittest

from rbs import cStrings

class TestSimpleDifferenceScoreFunction(unittest.TestCase):
    def test_basic(self):
        score = cStrings.simple_difference_score("ACG", "ACC")
        self.assertEqual(score, 2)

    def test_completely_different(self):
        score = cStrings.simple_difference_score("AAA", "CCC")
        self.assertEqual(score, 0)

class TestOverlapCountFunction(unittest.TestCase):
    def test_count_no_overlap(self):
        count = cStrings.overlap_count("GGAGG", "GG")
        self.assertEqual(count, 2)

    def test_count_with_overlap(self):
        count = cStrings.overlap_count("GGAGGAGG", "GGAGG")
        self.assertEqual(count, 2)

if __name__ == "__main__":
    unittest.main()
