# SPDX-FileCopyrightText: 2021 Konrad Weihmann
# SPDX-License-Identifier: GPL-2.0-only

import os
import sys


class TestBaseClass():

    TESTFILES_DIR = os.path.abspath(os.path.dirname(__file__) + "/../testfiles")
    TEST_UNDEFINED_PARAMETER = 'this is an undefined parameter to work around pytest limitations'

    @classmethod
    def setup_class(cls):
        sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/../"))

    def __pytest_empty_object_fixture(self, _input, default):
        if _input == TestBaseClass.TEST_UNDEFINED_PARAMETER:
            return default
        return _input

    def _create_args(self, inputfiles=[], preargs=[]):
        _args = self.__pytest_empty_object_fixture(preargs, [])
        _args += [*inputfiles]
        return self._create_args_parser().parse_args(_args)

    def _create_args_parser(self):
        from shellexeclist.__main__ import create_parser
        return create_parser()

    @staticmethod
    def file_in_testdir(file):
        if not file.startswith(TestBaseClass.TESTFILES_DIR):
            return os.path.join(TestBaseClass.TESTFILES_DIR, file.lstrip('/'))
        return file
