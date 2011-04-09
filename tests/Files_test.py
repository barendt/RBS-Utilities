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

    def test_directory_created_from_absolute_path(self):
        path = "{0}/git/RBS-Utilities/tests/foo".format(
            os.getenv("HOME"))
        Files.create_path_if_not_exists(path)
        self.assertTrue(os.path.exists(path))

    def test_directory_created_in_tmp(self):
        path = "/tmp/foo/"
        if os.path.exists(path):
            os.rmdir(path)
        Files.create_path_if_not_exists(path)
        self.assertTrue(os.path.exists(path))

if __name__ == "__main__":
    unittest.main()
