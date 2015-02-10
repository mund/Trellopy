"""
    Trellis: A trello mockup in Python
"""
import sys
import executioner

class Trellis(object):
    def __init__(self):
        # self.db = databox.box()
        self.execute = executioner.Executioner()
        # self.elements = ['board','list','card',
        #             'member','label','archive']
        self.command_list = ['display','create','rename','archive',
                    'getorder','reorder','move','assign', 'member']
        
    def begin(self):
        commands = self.parse_input(sys.argv)
        if commands:
            self.begin_executing(commands)

    def parse_input(self,cmd):
        if len(cmd) == 0:
            raise IndexError
        if len(cmd) == 1:
            self.print_help()
        else:
            return cmd[1:]
            
    def begin_executing(self,commands):
        action = commands[0]
        if len(commands) == 2:
            thing = commands[-1]
            if action == 'display':
                self.execute.task_display(thing)
            elif action == 'create':
                self.execute.task_create(thing)
            elif action == 'archive':
                self.execute.task_archive(thing)
            elif action == 'getorder':
                self.execute.task_getorder(thing)
            elif action == 'member':
                self.execute.task_add_member(thing)
            elif action in self.command_list:
                print "You provided two arguments, but the command needs three."
        elif len(commands) == 3:
            if action == 'rename':
                new_name = commands[-1]
                old_name = commands[-2]
                self.execute.task_rename(old_name, new_name)
            elif action == 'reorder':
                new_order = commands[-1]
                reorderme = commands[-2]
                self.execute.task_reorder(reorderme, new_order)
            elif action == 'move':
                target = commands[-1]
                source = commands[-2]
                self.execute.task_move(source,target)
            elif action == 'assign':
                assignee = commands[-1]
                assigned = commands[-2]
                self.execute.task_assign(assigned,assignee)
            elif action in self.command_list:
                print "You provided three arguments, but the command only takes two."
        else:
            self.print_help()

    def parse_two_commands(self,commands):
        pass

    def parse_three_commands():
        pass

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
                
                reorder     board/list              list1,list2,...,listN
                            board/list/card         card1,card2,...,cardN
                
                move        board/list/card         board/list
                
                assign      board/list/card         member_name

                member      member_name
"""
        print halp
        return halp