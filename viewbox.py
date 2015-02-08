import databox

class ViewBox(object):
	"""docstring for ViewBox"""
	def __init__(self):
		self.db = databox.box()

	def board(self, board_name):
		b = self.db.get_board(board_name)
		if b:
			print "Displaying board:",b['name']
			print b

	def blist(self,board_name,list_name):
		l = self.db.get_list(board_name,list_name)
		if l:
			print "Displaying list:",l['name']