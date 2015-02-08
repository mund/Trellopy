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

	def rename_board(self,board_name,new_name):
		result = self.boards.find({'name':board_name})[0]
		result['name'] = new_name
		print self.boards.update({'name':board_name},{'$set':result},upsert=False)

	def rename_list(self,board_name,list_name,new_name):
		result = self.boards.find({'name':board_name})[0]
		if result.get('lists'):
			l = result.get('lists')
			for d in l:
				if d['name'] == list_name:
					d['name'] = new_name
		print self.boards.update({'name':board_name},{'$set':result},upsert=False)

	def rename_card(self,board_name,list_name,card_name,new_name):
		result = self.boards.find({'name':board_name})[0]
		new_card = {'type':'card', 'name':card_name}
		if result.get('lists'):
			for l in result.get('lists'):
				if l['name'] == list_name:
					for c in l.get('cards'):
						if c['name'] == card_name:
							c['name'] = new_name
		print self.boards.update({'name':board_name}, 
				{'$set':result}, upsert=False)

	def archive_board(self,board_name):
		result = self.boards.find({'name':board_name})[0]
		result['archive'] = True
		print self.boards.update({'name':board_name}, 
				{'$set': result},upsert=False)

	def archive_list(self,board_name,list_name):
		result = self.boards.find({'name':board_name})[0]
		if result.get('lists'):
			l = result.get('lists')
			for d in l:
				if d['name'] == list_name:
					d['archive'] = True
		print self.boards.update({'name':board_name},{'$set':result},upsert=False)
	
	def archive_card(self,board_name,list_name,card_name):
		result = self.boards.find({'name':board_name})[0]
		new_card = {'type':'card', 'name':card_name}
		if result.get('lists'):
			for l in result.get('lists'):
				if l['name'] == list_name:
					for c in l.get('cards'):
						if c['name'] == card_name:
							c['archive'] = True
		print self.boards.update({'name':board_name}, {'$set':result}, upsert=False)

	def getorder(self,board_name,list_name=None):
		result = self.boards.find({'name':board_name})[0]
		if list_name:
			print "Getting card order for list",list_name,"in board",board_name
			for l in result.get('lists'):
				cards = l.get('cards')
				if cards:
					for c in cards:
						print c['name']
		else:
			for l in result.get('lists'):
				print l['name']
			
	def reorder(self,board_name,new_order,list_name=None):
		result = self.boards.find({'name':board_name})[0]
		if list_name:
			for each_list in result.get('lists'):
				cards = each_list.get('cards')
				if cards:
					inputed_card = new_order.split(',')
					each_list['cards'] = self.reorder_list(cards,inputed_card)
		else:
			current_list = result.get('lists')
			inputed_list = new_order.split(',')
			if len(current_list) == len(inputed_list):
				result['lists'] = self.reorder_list(current_list, inputed_list)
		print self.boards.update({'name':board_name}, {'$set':result}, upsert=False)

	def reorder_list(self,current_list, updated_list):
		return_list = []
		print updated_list
		for input_index in range(len(updated_list)):
			new_name = updated_list[input_index]
			# Look for item in current
			for dictionary in current_list:
				if dictionary['name'] == new_name:
					# Found it: target=dictionary,index=dict_index
					return_list.append(dictionary)
		return return_list

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
