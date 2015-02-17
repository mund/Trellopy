#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_trellis
----------------------------------

Tests for `trellis` module.
"""


class TestTrellis():
    def setUp(self):
        from trellis import trellis

    def test_create_board(self):
        control = trellis.BoardController()
        board = control.add_board('Bard')

    def tearDown(self):
        pass
