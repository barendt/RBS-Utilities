#!/usr/bin/env python

import unittest

from rbs import Strings

class TestAllIndicesFunction(unittest.TestCase):
    def setUp(self):
        self.haystack = "ACGTGTCACG"

    def test_no_occurrences(self):
        results = Strings.all_indices(self.haystack, "AAA")
        self.assertEqual(results, list())

    def test_one_occurrence(self):
        results = Strings.all_indices(self.haystack, "ACGT")
        self.assertEqual(results, [0])

    def test_two_occurrences(self):
        results = Strings.all_indices(self.haystack, "ACG")
        self.assertEqual(results, [0, 7])

if __name__ == "__main__":
    unittest.main()

