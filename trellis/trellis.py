# -*- coding: utf-8 -*-
from boards import Board
from members import Member
from backend import Operator
"""
Actions which can be performed on each item include:
    Boards can be:
        ✓created
        ✓renamed
        ✓archived
    Lists can be:
        ✓created,
        ✓archived,
        ✓renamed,
        reordered
    Cards can be:
        ✓created,
        ✓archived,
        ✓renamed,
        reordered within a list,
        ✓moved to another list
    Members can be:
        ✓created,
        ✓renamed,
        ✓archived,
        assigned to cards
    Labels can be:
        renamed,
        assigned to cards,
        One label per card
"""


class Controller(object):
    def __init__(self):
        self._operator = Operator()

    def new_board(self, board_name):
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

    # def get_board(self, board_name):
    #     pass
    #     # Get from DB

    # def archive_board(self, board_name):
    #     print "Fetching", board_name
    #     for b in _board_list:
    #         if b['name'] == board_name:
    #             return b.archive(board_name)
        # return Board.archive(board_name)

    # def add_member(self, member_name):
    #     member = Member(member_name)
    #     self.all_members.append(member)
    #     return member

    # def get_member(self, member_name):
    #     if member in self.all_members:
    #         if member.name == member_name:
    #             return member

    # def show(self):
    #     for brd in self.all_boards:
    #         print brd.show()

    # def make_label(self, label_name):
    #     # maximum of six
    #     if len(self.all_labels) != 6:
    #         self.all_labels.append(label_name)

    # def favor(self):
    #     manman = """
    #     [HOW-TO]
    #     import trellis
    #     board = trellis.new_board('New Board')
    #      OR board = trellis.get_board('Another Board')

    #     board.rename('Renamed Board')
    #     board.show()
    #     board.make_list('Some List')
    #     board.show_list('A List')
    #     board.archive()

    #     list = trellis.list_from_board(board_name,list_name)
    #     list.rename('')
    #     list.show()
    #     list.make_cards('')
    #     list.show_cards('')
    #     list.archive()

    #     card = trellis.card_from_list(board_name,list_name,card_name)
    #     card.rename('')
    #     card.show()
    #     card.make_cards('')
    #     card.archive()

    #     member = trellis.add_member('The Dude')
    #     member.assign_card()
    #     member.archive()
    #     member.rename('Rename')
    #     """
    #     return manman