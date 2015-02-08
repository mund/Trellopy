"""
    Trellis: A trello mockup in Python
"""
import sys
import databox

class Trellis(object):
    def __init__(self):
        self.db = databox.box()
        self.elements = ['board','list','card',
                    'member','label','archive']
        self.command_list = ['list','create','rename','archive',
                    'getorder','reorder','move','assign']
        
    def begin(self):
        command_line_argument_length = len(sys.argv)
        if command_line_argument_length == 0:
            raise IndexError
        if command_line_argument_length == 1:
            self.print_help()
        else:
            self.begin_executing(sys.argv[1:])

    def begin_executing(self,commands):
        action = commands[0]
        if action == 'create':
            # Should only have one argument
            self.task_create(commands[-1])
        elif action == 'rename':
            self.task_rename(commands[-2], commands[-1])
        elif action == 'archive':
            self.task_archive(commands[-1])
        elif action == 'getorder':
            self.task_getorder(commands[-1])
        elif action == 'reorder':
            self.task_reorder(commands[-2], commands[-1])
        elif action == 'move':
            self.task_move(commands[-2],commands[-1])
        elif action == 'assign':
            self.task_assign(commands[-2],commands[-1])
        elif action == 'member':
            self.task_member(commands[-1])
        else:
            self.print_help()

    def task_create(self,thing):
        if '/' in thing:
            if len(thing.split('/')) == 2:
                board,in_list = thing.split('/')
                self.db.create_list(board,in_list)
            if len(thing.split('/')) == 3:
                board,in_list,card = thing.split('/')
                self.db.create_card(board,in_list,card)
        else:
            self.db.create_board(thing)

    def task_rename(self, old_thing, new_name):
        if '/' in old_thing:
            if len(old_thing.split('/')) == 2:
                board_name,list_name = old_thing.split('/')
                self.db.rename_list(board_name,list_name,new_name)
            if len(old_thing.split('/')) == 3:
                board_name,list_name,card_name = old_thing.split('/')
                self.db.rename_card(board_name,list_name,card_name,new_name)
        else:
            self.db.rename_board(old_thing,new_name)

    def task_archive(self,thing):
        if '/' in thing:
            if len(thing.split('/')) == 2:
                board_name,list_name = thing.split('/')
                self.db.archive_list(board_name,list_name)
            if len(thing.split('/')) == 3:
                board_name,list_name,card_name = thing.split('/')
                self.db.archive_card(board_name,list_name,card_name)
        else:
            self.db.archive_board(thing)

    def task_getorder(self, thing):
        if '/' in thing:
            board_name,list_name = thing.split('/')
            self.db.getorder(board_name,list_name)
        else:
            self.db.getorder(thing)

    def task_reorder(self, thing, new_order):
        if '/' in thing:
            board_name,list_name = thing.split('/')
            #print "Reorder list",list_name,"in board",board_name,"with new order",new_order
            self.db.reorder(board_name,new_order,list_name)
        else:
            #print "Reorder",thing,"with new order",new_order
            self.db.reorder(thing,new_order)

    def task_move(self, source, destination):
        if len(source.split('/')) == 3 and len(destination.split('/')) == 2:
            self.db.move(source,destination)

    def task_member(self,member_name):
        self.db.add_member(member_name)

    def task_assign(self,boardlistcard,member):
        self.db.assign(boardlistcard,member)

    def list_all_the_things(self,thing):
        item = thing[:-1] # chop the 's'
        if item in self.elements:
            self.db.list_all(thing)

    def print_help(self):
        halp = """
python use.py   display     board
                            board/list
                            board/list/card

                create      board
                            board/list
                            board/list/card
                
                rename      board                   newname
                            board/list              newname
                            board/list/card         newname
                
                archive     board
                            board/list
                            board/list/card

                getorder    board
                            board/list
                
                reorder     board/list              list1,list2,...,listn
                            board/list/card         card1,card2,...,cardn
                
                move        board/list/card         board/list
                
                assign      board/list/card         member_name

                member      member_name
"""
        print halp