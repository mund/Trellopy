import pymongo


class Operator(object):
    def __init__(self):
        self._client = pymongo.MongoClient('mongodb://localhost:27017')
        self._db = self._client.potatodb
        self.boards = self._db.boards
        self.members = self._db.members
        self.boards.create_index('name', unique=True)
        self.members.create_index('name', unique=True)

    def save_board(self, board_dict):
        self.boards.insert(board_dict)

    def get_board(self, board_name):
        spec = {'name': board_name}
        try:
            return self.boards.find_one(spec)
        except Exception, e:
            print "Could not find board with name", board_name
            return False

    def update_board(self, board_data, board_name=None):
        spec = {}
        if board_name:
            spec['name'] = board_name
        else:
            spec['name'] = board_data['name']
        self.boards.update(spec, board_data)

    def gimme_everything(self):
        return self.boards.find()

    def gimme_everybody(self):
        return self.members.find()

    def new_member(self, member_dict):
        self.members.insert(member_dict)

    def update_member(self, member_data, member_name=None):
        spec = {}
        if member_name:
            spec['name'] = member_name
        else:
            spec['name'] = member_data['name']
        self.members.update(spec, member_data)

    def get_member(self, member_name):
        spec = {'name': member_name}
        try:
            return self.members.find_one(spec)
        except Exception, e:
            print "Could not find member with name", member_name
            return False
