import pymongo


class Operator(object):
    def __init__(self):
        self._client = pymongo.MongoClient('mongodb://localhost:27017')
        self._db = self._client.potatodb
        self.boards = self._db.boards
        self.boards.create_index('name', unique=True)

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
