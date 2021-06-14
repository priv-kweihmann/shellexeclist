# SPDX-FileCopyrightText: 2021 Konrad Weihmann
# SPDX-License-Identifier: GPL-3.0-only
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass


class TestClass0003(TestBaseClass):

    @pytest.mark.parametrize('kwargs', [{
        "inputfiles": [TestBaseClass.file_in_testdir('non-utf8')]
    }])
    def test_changeset_auto(self, kwargs):
        from shellexeclist.__main__ import run
        _res = run(self._create_args(**kwargs))

        import logging

        logging.warn(_res)

        assert _res == [
                '[', 
                'dirname', 
                'echo', 
                'install', 
                'ln', 
                'log_daemon_msg', 
                'log_end_msg', 
                'sh', 
                'sleep', 
                'start-stop-daemon', 
                'test'
                ]

    @pytest.mark.parametrize('kwargs', [{
        "inputfiles": [TestBaseClass.file_in_testdir('non-utf8')],
        "preargs": ['--forceshell=bash']
    }])
    def test_changeset_bash(self, kwargs):
        from shellexeclist.__main__ import run
        _res = run(self._create_args(**kwargs))

        assert _res == ['bash',
                        'dirname',
                        'install',
                        'ln',
                        'log_daemon_msg',
                        'log_end_msg',
                        'sleep',
                        'start-stop-daemon']
