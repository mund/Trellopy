import pymongo

class box(object):
	def __init__(self):
		self.client = pymongo.MongoClient("mongodb://localhost:27017/")
		self.database = self.client.stopgapdb
		self.boards = self.database.boards # This is a collection
		self.boards.create_index('name', unique=True)

	def create_board(self,board_name):
		board = {'type':'board','name':board_name}
		#result = self.boards.find({'type':'board','name':board_name,
		#						'lists':{},'cards': {},'assignee': ""})
		#if result.count() == 0:
		print "Creating board with name",board_name
		self.boards.insert({'type':'board','name':board_name})
		else:
			print "Another board with name",board_name,"already exists."

	def create_list(self,board_name,list_name):
		result = self.boards.find({'name':board_name})[0] 
		newlist = {'name':board_name, 'list': {'type':'list','name':list_name}}
		print 
		#self.boards.update({'name':board_name}, {'$set':newlist}, upsert=False)
		#print "Adding list",list_name,"to",result

	def create_card(self,board_name,list_name,card_name):
		result = self.boards.find({'name':board_name})[0]
		update = {'type':'board','name':board_name, 
					'list':{'name':list_name},
					'card':{'name':card_name}}
		self.boards.update({'name':board_name}, {'$set':update}, upsert=False)
		print "Creating card",card_name,"in list",list_name,"in board",board_name

	def rename_board(self,board_name,new_name):
		result = self.boards.find({'name':board_name})[0]
		update = {'type':'board','name':new_name}
		print self.boards.update({'name':board_name},{'$set':update},upsert=False)

	def rename_list(self,board_name,list_name,new_name):
		result = self.boards.find({'name':board_name})[0]
		update = { 'type':'board','name':board_name,
				   'list': {'type':'list', 'name':new_name}}
		print self.boards.update({'name':board_name},{'$set':update},upsert=False)

	def rename_card(self,board_name,list_name,card_name,new_name):
		result = self.boards.find({'name':board_name})[0]
		update = { 'type':'board','name':board_name,
				   'list': {'type':'list', 'name':list_name},
				   'card': {'type':'card', 'name':new_name}}
		print self.boards.update({'name':board_name},{'$set':update},upsert=False)

	def archive_board(self,board_name):
		result = self.boards.find({'name':board_name})[0]
		update = {'type':'board','archived':True}
		print self.boards.update({'name':board_name}, {'$set': update},upsert=False)

	def archive_list(self,board_name,list_name):
		result = self.boards.find({'name':board_name})[0]
		update = { 'type':'board','name':board_name,
				   'list': {'type':'list','name':list_name,'archived':True}}
		print self.boards.update({'name':board_name}, {'$set': update},upsert=False)
	
	def archive_card(self,board_name,list_name,card_name):
		result = self.boards.find({'name':board_name})[0]
		update = { 'type':'board','name':board_name,
				   'list': {'type':'list', 'name':list_name},
				   'card': {'type':'card', 'name':card_name, 'archived':True}}
		print self.boards.update({'name':board_name}, {'$set': update},upsert=False)