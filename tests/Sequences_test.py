#!/usr/bin/env python

import unittest

from rbs import Sequences

class TestGetBaseUsageFunction(unittest.TestCase):
    def test_some_of_every_base(self):
        usage = Sequences.get_base_usage("AGCUAGCU")
        self.assertEqual(usage["A"], 2)
        self.assertEqual(usage["C"], 2)
        self.assertEqual(usage["G"], 2)
        self.assertEqual(usage["U"], 2)

class TestHasInframeAugFunction(unittest.TestCase):
    def test_no_aug(self):
        self.assertFalse(Sequences.has_inframe_aug("AGGUCCUAGUAGGAUCU"))

    def test_out_of_frame_aug(self):
        self.assertFalse(Sequences.has_inframe_aug("AAUGGCUAGUAGGAUCU"))

    def test_in_frame_aug(self):
        self.assertTrue(Sequences.has_inframe_aug("AUGGCUAGUAAGGAUCU"))

class TestLoadFromDbFunction(unittest.TestCase):
    def test_no_db_throws_exception(self):
        self.assertRaises(Exception, Sequences.load_from_db, "foo.sqlite", 2)

    def test_uncleaned_record_count(self):
        db = "/Users/barendt/git/fresh_start/data/sequences.sqlite"
        sequences = Sequences.load_from_db(db, 11, 2, cleaned=False)
        self.assertEqual(len(sequences), 7525)

    def test_cleaned_record_count(self):
        db = "/Users/barendt/git/fresh_start/data/sequences.sqlite"
        sequences = Sequences.load_from_db(db, 11, 2)
        self.assertEqual(len(sequences), 5151)

class TestReverseComplementFunction(unittest.TestCase):
    def test_basic(self):
        rc = Sequences.reverse_complement("GGAGG")
        self.assertEqual(rc, "CCUCC")

if __name__ == "__main__":
    unittest.main()
