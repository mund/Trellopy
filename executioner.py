import databox
import viewbox

class Executioner(object):
    """Execute Command Line Arguments"""
    def __init__(self):
        self.db = databox.box()
        self.show = viewbox.ViewBox()
        
    def task_display(self,boardlistcard):
        if '/' in boardlistcard:
            if len(boardlistcard.split('/')) == 3:
                board_name,list_name,card_name = thing.split('/')
                self.show.blist(board_name,list_name)
            elif len(boardlistcard.split('/')) == 2:
                board_name,list_name = thing.split('/')
        else:
            self.show.board(boardlistcard)

    def task_add_member(self,member_name):
        self.db.add_member(member_name)

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

    def task_assign(self,boardlistcard,member):
        self.db.assign(boardlistcard,member)