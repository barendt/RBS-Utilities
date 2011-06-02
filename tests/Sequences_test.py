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
        sequences = Sequences.load_from_db(db, 11, 2, clean=False)
        self.assertEqual(len(sequences), 7525)

    def test_cleaned_record_count(self):
        db = "/Users/barendt/git/fresh_start/data/sequences.sqlite"
        sequences = Sequences.load_from_db(db, 11, 2)
        self.assertEqual(len(sequences), 5151)

class TestLoadRawRecordsFromDb(unittest.TestCase):
    def test_it_should_return_all_of_mid1_batch1(self):
        db = "/Users/barendt/git/fresh_start/data/sequences.sqlite"
        sequences = Sequences.load_raw_records_from_db(db, 1, 1)
        self.assertEqual(19646, len(sequences))

    def test_it_should_return_2_items_per_record(self):
        db = "/Users/barendt/git/fresh_start/data/sequences.sqlite"
        sequences = Sequences.load_raw_records_from_db(db, 1, 1)
        self.assertEqual(2, len(sequences[0]))

class TestMotifPositionCountsFunction(unittest.TestCase):
    def test_nothing(self):
        library = ("A"*18, "G"*18, "C"*18)
        motif = "UUU"
        results = Sequences.motif_position_counts(library, motif)
        self.assertEqual([0]*18, results)

    def test_GGAG(self):
        library = ("AGGAGCCATCTTCTATCT", "AGAAAGGAGTTATCCGAC")
        motif = "GGAG"
        expected = [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        results = Sequences.motif_position_counts(library, motif)
        self.assertEqual(expected, results)

    def test_GGAG_at_same_position(self):
        library = ("AGGAGCCATCTTCTATCT", 
                   "AGGAGAGAGTTATCCGAC")
        motif = "GGAG"
        expected = [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        results = Sequences.motif_position_counts(library, motif)
        self.assertEqual(expected, results)

class TestRBSLibraryNamedTuple(unittest.TestCase):
    def test_it_can_be_created_and_referenced(self):
        library = Sequences.RBSLibrary(1, 2)
        self.assertEqual(1, library.batch)
        self.assertEqual(2, library.mid)

class TestReverseComplementFunction(unittest.TestCase):
    def test_basic(self):
        rc = Sequences.reverse_complement("GGAGG")
        self.assertEqual(rc, "CCUCC")

if __name__ == "__main__":
    unittest.main()
