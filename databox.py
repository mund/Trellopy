import pymongo

class box(object):
	def __init__(self):
		self.client = pymongo.MongoClient("mongodb://localhost:27017/")
		self.database = self.client.stopgapdb
		self.boards = self.database.boards # This is a collection
		self.boards.create_index('name', unique=True)

	def create_board(self,board_name):
		try:
			board = {'type':'board','name':board_name}
			self.boards.insert({'type':'board','name':board_name})
		except pymongo.errors.DuplicateKeyError, e:
			print "Another board with name",board_name,"already exists."	

	def create_list(self,board_name,list_name):
		result = self.boards.find({'name':board_name})[0] 
		new_list = {'type':'list','name':list_name}
		if result.get('lists'):
			result['lists'].append(new_list)
		else:
			result['lists'] = [new_list,]
		self.boards.update({'name':board_name}, {'$set':result})

	def create_card(self,board_name,list_name,card_name):
		result = self.boards.find({'name':board_name})[0]
		new_card = {'type':'card', 'name':card_name}
		if result.get('lists'):
			for l in result.get('lists'):
				if l['name'] == list_name:
					if l.get('cards'):
						l.get('cards').append(new_card)
					else:
						l['cards'] = [new_card,]
		print self.boards.update({'name':board_name}, {'$set':result}, upsert=False)

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
		print self.boards.update({'name':board_name}, {'$set':result}, upsert=False)

	def archive_board(self,board_name):
		result = self.boards.find({'name':board_name})[0]
		result['archive'] = True
		print self.boards.update({'name':board_name}, {'$set': result},upsert=False)

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