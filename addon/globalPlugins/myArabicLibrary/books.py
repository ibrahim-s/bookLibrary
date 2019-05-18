#for compatibility with python3
try:
	import cPickle as pickle
except ImportError:
	import pickle

#.decode("mbcs")

import os

CURRENT_DIR= os.path.dirname(__file__).decode("mbcs")
SAVING_DIR= os.path.join(CURRENT_DIR, "..", "..", "mydata")

class Book(object):
	myBooks={}
	filename= ""

	def __init__(self, name, author, about, size, url, url2):
		super(Book, self).__init__()
		self.key= (name, author)
		self.name= name
		self.author= author
		self.about= about
		self.size= size
		self.url= url
		self.url2= url2

	@classmethod
	def add_book(cls, name, author, about, size, url, url2):
		book= cls(name, author, about, size, url, url2)
		cls.myBooks[book.key]= {"about": book.about, "size": book.size, "url": book.url, "url2": book.url2}
		#print cls.myBooks
		#cls.save_to_file()

	@classmethod
	def remove_book(cls, bookKey):
		'''removing a book with the help of the book key.'''
		del cls.myBooks[bookKey]
		if not cls.myBooks:
			cls.save_to_file()

	@classmethod
	def remove_allBooks(cls):
		if not cls.myBooks:
			return
		cls.myBooks.clear()
		cls.save_to_file()

	@classmethod
	def save_to_file(cls):
		with open(os.path.join(SAVING_DIR, cls.filename), 'wb') as f:
			#print cls.myBooks
			pickle.dump(cls.myBooks, f)
		cls.myBooks= {}
			#print cls.myBooks

	@classmethod
	def retreave_from_file(cls):
		if cls.myBooks: return
		else:
			try:
				with open(os.path.join(SAVING_DIR, cls.filename), 'rb') as f:
					d= pickle.load(f)
					cls.myBooks= d
			except:
				cls.myBooks= {}

	@classmethod
	def getBookByKey(cls, key):
		book= cls(key[0], key[1], cls.myBooks[key]['about'], cls.myBooks[key]['size'], cls.myBooks[key]['url'], cls.myBooks[key]['url2'])
		return book

	@classmethod
	def getBookByUrl(cls, url):
		key= [key for key in cls.myBooks if cls.myBooks[key]['url']== url]
		if key:
			book= cls.getBookByKey(key[0])
			return book

	@classmethod
	def getBookByUrl2(cls, url):
		key= [key for key in cls.myBooks if cls.myBooks[key]['url2']== url]
		if key:
			book= cls.getBookByKey(key[0])
			return book

if __name__== '__main__':
	#Book.add_book('book1', 'author1', 'about1', 'size1', 'url1', 'url2')
	#Book.save_to_file()
	Book.retreave_from_file('test.pickle')
	print Book.myBooks