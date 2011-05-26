#!/usr/bin/env python

import unittest

from rbs.UNAFold import UnafoldSequence

class TestUnafoldSequence(unittest.TestCase):
    def setUp(self):
        sequence = 'GGGACACCACAACGGUUUCCCUAAUUCCCU'
        self.u = UnafoldSequence(sequence)

    def test_it_folds_itself_when_dG_is_requested(self):
        self.assertEqual(-11.1, self.u.dG)

    def test_it_should_give_the_correct_dG(self):
        self.u.fold()
        self.assertEqual(-11.1, self.u.dG)


if __name__ == "__main__":
    unittest.main()

