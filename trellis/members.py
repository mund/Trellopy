class Member(object):
    """docstring for Member"""
    def __init__(self, arg):
        self.name = None

    def add_member(self, member_name):
        self.name = member_name
        return self
