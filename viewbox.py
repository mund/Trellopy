import databox

class ViewBox(object):
	"""docstring for ViewBox"""
	def __init__(self):
		self.db = databox.box()

	def board(self, board_name):
		board = self.db.get_board(board_name)
		if board:
			self.show(board)

	def blist(self,board_name,list_name):
		lisst = self.db.get_list(board_name,list_name)
		if lisst:
			self.show(lisst)

	def bcard(self,board_name,list_name,card_name):
		card = self.db.get_card(board_name,list_name,card_name)
		if card:
			self.show(card)

	def show(self,item):
		item_keys = item.keys()
		while item_keys:
			key = item_keys.pop()
			if key == "_id":
				print "id:",item[key]
			elif key == 'lists':
				print "[LISTS]"
				list_list = item['lists']
				self.show_lists(list_list)
			elif key == 'cards':
				print "[CARDS]"
				cards_list = item['cards']
				self.show_cards(cards_list)
			else:
				print key+":",item[key]

	def show_lists(self,listlist):
		for lizt in listlist:
			lk = lizt.keys()
			while lk:
				k = lk.pop()
				if k == 'cards':
					print "\t[CARDS]"
					cl = lizt['cards']
					self.show_cards(cl,extratab=True)
				else:
					print "\t",k+":",lizt[k]
			print ""

	def show_cards(self,cardlist,extratab=False):
		for card in cardlist:
			ck = card.keys()
			while ck:
				k = ck.pop()
				if extratab: print "\t\t",k+":",card[k]
				else: print "\t",k+":",card[k]
			print ""