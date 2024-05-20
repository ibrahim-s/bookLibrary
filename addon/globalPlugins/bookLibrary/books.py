# -*- coding: utf-8 -*-
# books.py
# Copyright 2019 ibrahim hamadeh, released under GPLv2.0
# See the file COPYING for more details
# This module is aimed to construct book object, retreave books from file, save books to file and use other helpful functions.

import wx, gui
import os
import json
from logHandler import log

CURRENT_DIR= os.path.dirname(__file__)
SAVING_DIR= os.path.join(os.path.expanduser('~'), 'bookLibrary-addonFiles')

class Book(object):
	myBooks={}
	filename= ""

	def __init__(self, name, author, about, size, url, otherUrls):
		super(Book, self).__init__()
		self.key = str((name, author))
		self.name= name
		self.author= author
		self.about= about
		self.size= size
		self.url= url
		self.otherUrls= otherUrls

	@classmethod
	def add_book(cls, name, author, about, size, url, otherUrls):
		'''Adding a book to a library.'''
		book= cls(name, author, about, size, url, otherUrls)
		cls.myBooks[book.key]= {"about": book.about, "size": book.size, "url": book.url, "otherUrls": book.otherUrls}

	@classmethod
	def remove_book(cls, bookKey):
		'''removing a book with the help of the book key.'''
		del cls.myBooks[str(bookKey)]
		if not cls.myBooks:
			cls.save_to_file()

	@classmethod
	def remove_allBooks(cls):
		''' Removing all books from a library.'''
		if not cls.myBooks:
			return
		cls.myBooks.clear()
		cls.save_to_file()

	# save data
	@classmethod
	def save_to_file(cls):
		try:
			with open(os.path.join(SAVING_DIR, cls.filename), 'w', encoding= 'utf-8') as f:
				json.dump(cls.myBooks, f, ensure_ascii= False, indent= 4)
			cls.myBooks= {}
		except Exception as e:
			#log.info("Error",exc_info=1)
			raise e

	#retreave data
	@classmethod
	def retreave_from_file(cls):
		'''Retreaving books from a specific library file.'''
		if cls.myBooks: return
		try:
			with open(os.path.join(SAVING_DIR, cls.filename), encoding= 'utf-8') as f:
				d= json.load(f)
				cls.myBooks= d
		except Exception as e:
			# Translators: Message displayed when getting an error trying to retreave books data
			gui.messageBox(_("Unable to load books data"), 
			# Translators: Title of message box
			_("Error"), wx.OK|wx.ICON_ERROR)
			log.info("Error", exc_info= True)
			return

	@classmethod
	def getBookByKey(cls, key):
		#log.info(f'cls.myBooks: {cls.myBooks}')
		#changing to json , the key needs to be a string
		name, author = key[0], key[1]
		key= str(key)
		if not key in cls.myBooks:
			return
		book= cls(name, author, cls.myBooks[key]['about'], cls.myBooks[key]['size'], cls.myBooks[key]['url'], cls.myBooks[key]['otherUrls'])
		return book

	@classmethod
	def getBookByUrl(cls, url):
		key= [key for key in cls.myBooks if cls.myBooks[key]['url']== url]
		if key:
			book= cls.getBookByKey(eval(key[0]))
			return book
