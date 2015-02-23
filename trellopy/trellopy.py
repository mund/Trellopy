# -*- coding: utf-8 -*-
"""
.. module:: trellopy

.. moduleauthor:: Amol Mundayoor <amol.com@gmail.com>
"""
from boards import Board
from members import Member
from backend import Operator
# """
# Actions which can be performed on each item include:
#     Boards can be:
#         ✓created
#         ✓renamed
#         ✓archived
#     Lists can be:
#         ✓created,
#         ✓archived,
#         ✓renamed,
#         ✓reordered
#     Cards can be:
#         ✓created,
#         ✓archived,
#         ✓renamed,
#         ✓reordered within a list,
#         ✓moved to another list
#     Members can be:
#         ✓created,
#         ✓renamed,
#         ✓archived,
#         ✓assigned to cards
#     Labels can be:
#         ✓renamed,
#         ✓assigned to cards,
#         ✓One label per card
# """


class Controller(object):
    def __init__(self):
        """
        Initializes a connection to the PyMongo Database.
        """
        self._operator = Operator()

    def new_board(self, board_name):
        """
        Create a new board with name <board_name>.

        :param name: The name you want the board to have.
        :returns: A Board class, with name attribute <board_name>
        """
        return Board(board_name)

    def get_board(self, board_name):
        board_data = self._operator.get_board(board_name)
        return Board(board_name, board_data)
        # return Board(board_name)

    def show_boards(self):
        everything = self._operator.gimme_everything()
        for each in everything:
            print "Board Name:", each['name']
            print "Archived:  ", each['archived']
            all_lists = each['lists']
            if all_lists:
                for single in all_lists:
                    print "  List Name:", single['name']
            # print "Lists:     ", each['lists']

    def new_member(self, member_name):
        return Member(member_name)

    def get_member(self, member_name):
        return Member(member_name)

    def show_members(self):
        everybody = self._operator.gimme_everybody()
        for body in everybody:
            print body
