"""
test_trellis
----------------------------------

Tests for `boards` module.
"""
from trellis.boards import Board
class TestBoards():
    def setUp(self):
  		pass

    def test_rename(self):
    	brd = Board("Simple Board")
        brd.rename("Renamed")
        assert brd.name == "Renamed"

    def tearDown(self):
        pass