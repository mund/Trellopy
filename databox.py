import pymongo

class box(object):
	def __init__(self):
		self.client = pymongo.MongoClient("mongodb://localhost:27017/")
		self.database = self.client.stopgapdb
		self.boards = self.database.boards # This is a collection
		self.members = self.database.members
		self.boards.create_index('name', unique=True)
		self.members.create_index('name',unique=True)

	def get_board(self,board_name):
		try:
			return self.boards.find({'name':board_name})[0]
		except IndexError, e:
			print "Could not find board with name:",board_name
	def get_list(self,board_name,list_name):
		try:
			board = self.boards.find({'name':board_name})[0]
			lists = board.get('lists')
			if lists:
				for one_list in lists:
					if one_list['name'] == list_name:
						return one_list
		except IndexError, e:
			print "Could not find board with name:",board_name
	def get_order(self,board_name,list_name=None):
		try:
			result = self.boards.find({'name':board_name})[0]
			lists = result.get('lists')
			if list_name and lists:
				for l in lists:
					if l['name'] == list_name:
						cards = l.get('cards')
						if cards:
							for c in cards:
								print c['name']
							return True
						else:
							print "No cards found in list",list_name
							return None
				print "Could not find list",list_name
			else:
				if lists:
					for l in lists:
						print l['name']
				else:
					print "No lists found in board",board_name
		except IndexError, e:
			print "Could not find board with name",board_name

	def create_board(self,board_name):
		try:
			self.boards.insert({'type':'board','name':board_name})
			print "Successfully created board with name",board_name+"."
		except pymongo.errors.DuplicateKeyError, e:
			print "Another board with name",board_name,"already exists."
	def create_list(self,board_name,list_name):
		result = self.boards.find({'name':board_name})[0] 
		new_list = {'type':'list','name':list_name}
		all_list = result.get('lists')
		if all_list:
			for single in all_list:
				if single['name'] == list_name:
					print "A list with name",list_name,"already exists in board",board_name
					return None
			all_list.append(new_list)
		else:
			result['lists'] = [new_list,]
		print "Adding list",list_name,"to board",board_name
		self.boards.update({'name':board_name}, {'$set':result})
	def create_card(self,board_name,list_name,card_name):
		result = self.boards.find({'name':board_name})[0]
		new_card = {'type':'card', 'name':card_name}
		all_list = result.get('lists')
		if all_list:
			for single in all_list:
				if single['name'] == list_name:
					cards = single.get('cards')
					if cards:
						for card in cards:
							if card['name'] == card_name:
								print "A card with name",card_name,"already exists in list",list_name,"in board",board_name
								return None
						cards.append(new_card)
					else:
						single['cards'] = [new_card,]
					print "Adding card",card_name,"to list",list_name,"in board",board_name
					self.boards.update({'name':board_name}, {'$set':result}, upsert=False)
					return True
				else:
					print "Could not find list",list_name
		
	def rename_board(self,board_name,new_name):
		try:
			result = self.boards.find({'name':board_name})[0]
			result['name'] = new_name
			self.boards.update({'name':board_name},
					{'$set':result},upsert=False)
			print "Successfully renamed board",board_name,"to",new_name
			return True
		except IndexError:
			print "Could not find board with name",board_name
		except pymongo.errors.DuplicateKeyError, e:
			print "Another board with name",board_name,"already exists."
	def rename_list(self,board_name,list_name,new_name):
		try:
			result = self.boards.find({'name':board_name})[0]
			if result.get('lists'):
				lists = result.get('lists')
				for card in lists:
					if card['name'] == list_name:
						card['name'] = new_name
						self.boards.update({'name':board_name},
							{'$set':result},upsert=False)
						print "Successfully renamed list",list_name,"to",new_name
						return True
			print "Could not find list",list_name,"in board",board_name
		except IndexError:
			print "Could not find board with name",board_name
		except pymongo.errors.DuplicateKeyError, e:
			print "A list with name",list_name,"already exists in board",board_name
	def rename_card(self,board_name,list_name,card_name,new_name):
		try:
			result = self.boards.find({'name':board_name})[0]
			new_card = {'type':'card', 'name':card_name}
			if result.get('lists'):
				for each_list in result.get('lists'):
					if each_list['name'] == list_name:
						for card in each_list.get('cards'):
							if card['name'] == card_name:
								card['name'] = new_name
								self.boards.update({'name':board_name}, 
									{'$set':result}, upsert=False)
								print "Successfully renamed card",card_name,"to",new_name
								return True
						print "Could not find card",card_name,"not found in list",list_name
		except pymongo.errors.DuplicateKeyError, e:
			print "A card with name",card_name,"already exists in list",list_name,"in board",board_name

	def archive_board(self,board_name):
		try:
			result = self.boards.find({'name':board_name})[0]
			result['archive'] = True
			self.boards.update({'name':board_name}, 
				{'$set': result},upsert=False)
			print "Archived board:",board_name
		except IndexError, e:
			print "Could not find board with name",board_name
	def archive_list(self,board_name,list_name):
		result = self.boards.find({'name':board_name})[0]
		if result.get('lists'):
			lists = result.get('lists')
			for each_list in lists:
				if each_list['name'] == list_name:
					each_list['archive'] = True
					self.boards.update({'name':board_name},\
						{'$set':result},upsert=False)
					print "Archived list:",list_name
					return True
			print "Could not find list with name",list_name
		else:
			print "Board",board_name,"does not have list with name",list_name
	def archive_card(self,board_name,list_name,card_name):
		result = self.boards.find({'name':board_name})[0]
		new_card = {'type':'card', 'name':card_name}
		if result.get('lists'):
			for l in result.get('lists'):
				if l['name'] == list_name:
					for c in l.get('cards'):
						if c['name'] == card_name:
							c['archive'] = True
							self.boards.update({'name':board_name}, 
								{'$set':result}, upsert=False)
							print "Archived card",card_name
							return True
					print "Could not find card",card_name
					return None
			print "Could not find list",list_name
			return None
		else:
			print "Board",board_name,"does not have a list with name",list_name

	def reorder(self,board_name,new_order,list_name=None):
		result = self.boards.find({'name':board_name})[0]
		if list_name:
			for each_list in result.get('lists'):
				cards = each_list.get('cards')
				if cards:
					inputed_card = new_order.split(',')
					if len(inputed_card) == len(cards):
						returned_list = self.reorder_helper(cards,inputed_card)
						if returned_list:
							self.boards.update({'name':board_name}, {'$set':result}, upsert=False)
							print "Updated cards in list",list_name,"with order",new_order
							return True
						else:
							print "At least one card was not found. No changes made."
					else:
						print "Input order should be card names, comma separated, no spaces.\n"
						print "For example, if you would like to reorder cards in board/list:"
						print "python use.py reorder board/list card3,card1,card2,car4,card5\n"
						print "Use the command getorder to get names and total count, like so:"
						print "python use.py getorder [(board)|(board/list)] for lists or cards."
		else:
			current_list = result.get('lists')
			inputed_list = new_order.split(',')
			if len(current_list) == len(inputed_list):
				returned_list = self.reorder_helper(current_list, inputed_list)
				if returned_list:
					self.boards.update({'name':board_name}, {'$set':result}, upsert=False)
					print "Updated lists in board",board_name,"with order",new_order
				else:
					print "At least one card was not found. Aborting!"
			else:
				print "Input order should be card names, comma separated, no spaces.\n"
				print "For example, if you would like to reorder cards in board/list:"
				print "python use.py reorder board/list card3,card1,card2,car4,card5\n"
				print "Use the command getorder to get names and total count, like so:"
				print "python use.py getorder [(board)|(board/list)] for lists or cards."
	def reorder_helper(self,current_list, updated_list):
		return_list = []
		for input_index in range(len(updated_list)):
			list_name = updated_list[input_index]
			for each_list in current_list:
				if each_list['name'] == list_name:
					return_list.insert(input_index,each_list)
		if len(return_list) == len(current_list):
			return return_list
		else:
			return None

	def move(self,boardlistcard,boardlist):
		dest_card = self.fetch_card(boardlistcard)
		self.move_card(dest_card,boardlist)
	def move_card(self,card,boardlist):
		board_name,list_name = boardlist.split('/')
		result = self.boards.find({'name':board_name})[0]
		lists = result.get('lists')
		if lists:
			for each_list in lists:
				if each_list['name'] == list_name:
					cards = each_list.get('cards')
					if cards:
						cards.append(card)
					else:
						each_list['cards'] = [cards,]
		print self.boards.update({'name':board_name}, {'$set':result}, upsert=False)
	def fetch_card(self,boardlistcard):
		board_name,list_name,card_name = boardlistcard.split('/')
		result = self.boards.find({'name':board_name})[0]
		lists = result.get('lists')
		if lists:
			for each_list in lists:
				if list_name == each_list['name']:
					cards = each_list.get('cards')
					if cards:
						for card in cards:
							if card['name'] == card_name:
								return card

	def assign(self,boardlistcard,member):
		board_name,list_name,card_name = boardlistcard.split('/')
		result = self.boards.find({'name':board_name})[0]
		lists = result.get('lists')
		if lists:
			for each_list in lists:
				if list_name == each_list['name']:
					cards = each_list.get('cards')
					if cards:
						for card in cards:
							if card['name'] == card_name:
								card['assignee'] = member
		print self.boards.update({'name':board_name}, {'$set':result}, upsert=False)

	def add_member(self,member_name):
		try: 
			self.members.insert({'type':'member','name':member_name})
			print "Successfully created member with name",member_name+"."
		except pymongo.errors.DuplicateKeyError, e:
			print "Another member with name",member_name,"already exists."	
