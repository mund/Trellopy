from backend import Operator


class Board(object):
    """
    BOARD:  When initialized, a simple dict is saved to the database.
            board = {
                'name': <board_name>
                'lists': <list_of_boardlist>
                'archived': <true|false>
            }
    """
    def __init__(self, name):
        self._operator = Operator()
        if not self.in_database(name):
            self.board = {}
            self.board['name'] = name
            self.board['lists'] = None
            self.board['archived'] = False
            self._operator.save_board(self.board)
        else:
            self.board = self._operator.get_board(name)

    def rename(self, new_name):
        old_name = self.board['name']
        self.board['name'] = new_name
        self._operator.update_board(self.board, old_name)

    def archive(self):
        self.board['archived'] = True
        self._operator.update_board(self.board)

    def add_list(self, list_name):
        if not self.board['lists']:
            self.board['lists'] = []
        parent_board = self.board['name']
        new_list_item = BoardList(board=parent_board, name=list_name)
        self.board['lists'].append(new_list_item.lizt)
        self._operator.update_board(self.board)
        return new_list_item

    def get_list(self, list_name):
        for lizt in self.board['lists']:
            if lizt['name'] == list_name:
                list_from_dict = BoardList(from_dict=lizt)
                return list_from_dict

    def in_database(self, name):
        return self._operator.get_board(name)

    def __repr__(self):
        return "<Board: "+self.board['name']+">"

    def get_board(self, board_name):
        return self._operator.get_board(board_name)

    def update_board(self):
        self._operator.update_board(self.board)

    # def show(self):
    #     print "Board Name:", self.name
    #     if self.board_list:
    #         print "  [LISTS]"
    #         for each_list in self.board_list:
    #             # if each_list:
    #             print "  ", each_list.show()

    # def get_list_order(self):
    #     return self.board_list

    # def set_list_order(self, order):
    #     print "New order:", order

    # def save(self):
    #     return True

    # def itself(self):
    #     return self


class BoardList(object):
    """
    LIST:  A List class is represented as follows in the database:
            lists = [{
                'board': <board_name>
                'name': <list_name>
                'cards': <list_of_boardlistcard>
                'archived': <true|false>
            }]
    """

    def __init__(self, from_dict=None, *tuples, **dicts):
        if not from_dict:
            self.lizt = {}
            self.lizt['board'] = dicts.get('board')
            self.lizt['name'] = dicts.get('name')
            self.lizt['cards'] = None
            self.lizt['archived'] = False
        if from_dict:
            self.lizt = from_dict

    def archive(self):
        self.lizt['archived'] = True
        return self

    def rename(self, new_name):
        old_name = self.lizt['name']
        self.lizt['name'] = new_name
        return self

    def add_card(self, card_name):
        if not self.list_cards:
            self.list_cards = []
        new_card = BoardListCard(card_name)
        self.list_cards.append(new_card)
        return new_card

    def show(self):
        print "  List Name:", self.name
        if self.list_cards:
            for each_card in self.list_cards:
                print "    ", each_card

    def __repr__(self):
        return "  <List: " + self.lizt['name']+">"


class BoardListCard(object):
    """docstring for BoardListCard"""
    def __init__(self, name):
        self.name = name
        self.feat = None

    def rename(self, new_name):
        self.name = new_name
        return self

    def add_feature(self, features):
        # `features` must be dict
        if not self.feat:
            self.feat = []
        self.feat.append(features)

    def archive(self, name):
        print "Archiving card", name

    def assign_to(self, member_name):
        print "Assigning", self.name, "to", member_name

    def mark_with(self, label_name):
        print "Marking", self.name, "as", label_name

    def __repr__(self):
        return "    <Card: "+self.name+">"

    def __str__(self):
        return "    Card: "+self.name

    def show(self):
        # if self.name:
        print "    Card Name:", self.name
        if self.features:
            for key, value in features:
                print key, value
