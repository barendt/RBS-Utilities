#!/usr/bin/env python

import os
import unittest

from rbs import Files

class TestCreatePathIfNotExistsFunction(unittest.TestCase):
    def test_directory_created(self):
        if os.path.exists("tmp"):
            os.rmdir("tmp")
        Files.create_path_if_not_exists("tmp")
        self.assertTrue(os.path.exists("tmp"))

    def test_directory_created_from_full_path(self):
        """TODO: Don't hardcode the full path, generate one."""
        path = "/Users/barendt/git/RBS-Utilities/tests/foo"
        Files.create_path_if_not_exists(path)
        self.assertTrue(os.path.exists(path))

if __name__ == "__main__":
    unittest.main()
