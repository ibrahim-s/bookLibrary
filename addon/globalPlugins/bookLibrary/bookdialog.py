# -*- coding: utf-8 -*-
#bookdialog.py
# Copyright (C) 2019 ibrahim hamadeh, released under GPLv2.0
#graphical user interface for book dialog

import wx, gui
import webbrowser
import os
import api
import queueHandler
from .books import Book
import json
from logHandler import log

import addonHandler
addonHandler.initTranslation()

def getBookName(message, caption, book= None):
	"Allowing the user to enter the book name, upon adding a book or editing one."
	dlg= wx.TextEntryDialog(None, message, caption)
	if book:
		dlg.SetValue(book.name)
	dlg.ShowModal()
	result= dlg.GetValue().strip()
	if  result:
		return result
	else:
		gui.messageBox(
		# Translators: message displayed when the user leaves the book name entry blank.
		_('Name required; You can not leave it blank'), 
		_('information'))
		return getBookName(message, caption, book)

def getBookAuthor(message, caption, book= None):
	dlg= wx.TextEntryDialog(None, message, caption)
	if book:
		dlg.SetValue(book.author)
	dlg.ShowModal()
	result= dlg.GetValue().strip()
	return result

def getBookAbout(message, caption, book= None):
	dlg= wx.TextEntryDialog(None, message, caption, style= wx.OK | wx.CANCEL|wx.TE_MULTILINE)
	if book:
		dlg.SetValue(book.about)
	dlg.ShowModal()
	result= dlg.GetValue().strip()
	return result

def getBookSize(message, caption, book= None):
	dlg= wx.TextEntryDialog(None, message, caption)
	if book:
		dlg.SetValue(book.size)
	dlg.ShowModal()
	result= dlg.GetValue().strip()
	return result

def getBookUrl(message, caption, book= None):
	dlg= wx.TextEntryDialog(None, message, caption)
	if book:
		dlg.SetValue(book.url)
	dlg.ShowModal()
	result= dlg.GetValue().strip()
	if not result:
		gui.messageBox(
		# Translators: message displayed when the user did not enter a url.
		_('You can not leave this blank, please enter a url.'), 
		_('Information'))
		return getBookUrl(message, caption, book)
	return result

def getBookOtherUrls(message, caption, book= None):
	dlg= wx.TextEntryDialog(None, message, caption, style= wx.OK | wx.CANCEL|wx.TE_MULTILINE)
	if book:
		dlg.SetValue(book.otherUrls)
	dlg.ShowModal()
	result= dlg.GetValue().strip()
	return result

#the popup menu class
class MyPopupMenu(wx.Menu):
	def __init__(self, parent, eventObjectId):
		super(MyPopupMenu, self).__init__()
        
		self.parent = parent
		#log.info(f'self.parent.libraryDirectory: {self.parent.libraryDirectory}')
		self.eventObjectId= eventObjectId

#add a subMenu for change sorting of book
		subMenu= wx.Menu()
		self.sortByName = subMenu.Append(wx.ID_ANY, 
		# Translators: label of men to sort books according to book name.
		_('Sort Books By Name'), kind=wx.ITEM_CHECK)
		self.sortByAuthor = subMenu.Append(wx.ID_ANY, 
		# Translators: label of menu to sort books according to author name.
		_('Sort Books By Author'), kind=wx.ITEM_CHECK)
		self.AppendSubMenu(subMenu, 
		# Translators: label obj subMenu items for sorting books.
		_('Sort Books By'))
		self.Bind(wx.EVT_MENU, self.onSortByName, self.sortByName)
		self.Bind(wx.EVT_MENU, self.onSortByAuthor, self.sortByAuthor)
		# in online libraries we only need sort by menu.
		if not self.parent.isLocalLibrary:
			return

		#Add A Book menu
		add= wx.MenuItem(self, -1, 
		# Translators: label obj menu items to add a book.
		_('Add A Book'))
		self.Append(add)
		self.Bind(wx.EVT_MENU, self.onAdd, add)

		#Edit Selected Book menu
		edit= wx.MenuItem(self, -1, 
		# Translators: label of menu items to edit a book.
		_('Edit Selected '))
		self.Append(edit)
		self.Bind(wx.EVT_MENU, self.onEdit, edit)

		#Remove Selected Book menu
		remove= wx.MenuItem(self, -1, 
		# Translators: label of menu items to remove a book.
		_('Remove Selected '))
		self.Append(remove)
		self.Bind(wx.EVT_MENU, self.onRemove, remove)

		#add a subMenu for moving a book
		subMenu= wx.Menu()
		# We want to append to this menu library names.
		libraryNames= BookDialog.libraryFiles
		libraryMenus= (name for name in libraryNames if name!= BookDialog.activeLibrary)
		#log.info(f'libraryMenus: {list(libraryMenus)}')
		# appending library menus to subMenu.
		for label in libraryMenus:
			item= subMenu.Append(wx.ID_ANY, label)
			self.Bind(wx.EVT_MENU, lambda evt , args=label : self.onMoveBook(evt, args), item)
		self.AppendSubMenu(subMenu, 
		# Translators: label obj subMenu items for moving a book.
		_('Move Book To'))

		#Remove All Books menu
		removeAll= wx.MenuItem(self, -1, 
		# Translators: label of menu items to remove all books.
		_('Remove All '))
		self.Append(removeAll)
		self.Bind(wx.EVT_MENU, self.onRemoveAll, removeAll)

	def onSortByAuthor(self, evt):
		if not BookDialog.sortByAuthor:
			self.parent.populateListBox(sortByAuthor=True)
			self.parent.focusAndSelect()
			BookDialog.sortByAuthor= True

	def onSortByName(self, evt):
		if BookDialog.sortByAuthor:
			self.parent.populateListBox()
			self.parent.focusAndSelect()
			BookDialog.sortByAuthor= False
		else: pass

	def onAdd(self, e= None, book= None):
		name=getBookName(_('EnterBook Name Please'), 
		_('Book Name'), book)
		#log.info('name: %s'%name)

		#getting the author
		author= getBookAuthor(_('Enter Author Name'), 
		_('Author name'), book)
		#log.info('author: %s'%author)
		#if (name, author) in Book.myBooks:
		if str((name, author)) in Book.myBooks:
			# Translators: message displayed if book is already present in library.
			gui.messageBox(_("This book already exist in library, please enter a new one or remove existed first"),
			# Translators: Title of message box.
			_("Warning"))
			return
		#getting the about of the book
		about= getBookAbout(_("Write Something About The Book"), 
		_("About"), book)

		#getting size of book
		size= getBookSize(_("Enter Size of Book or file"), 
		_("size"), book)
		#log.info('size: %s'%size)

		#getting the url of the book
		url= getBookUrl(_('Enter Url source to access book(www...)'), 
		_('Url:'), book)
		#log.info('url: %s'%url)

		#getting book Other urls
		otherUrls= getBookOtherUrls(_('Enter other urls for the book if present, or leave blank'), 
		_('Othr urls:'), book)
		Book.add_book(name, author, about, size, url, otherUrls)
		sortingFlag= BookDialog.sortByAuthor
		self.parent.populateListBox(sortingFlag)
		self.parent.focusAndSelect(bookKey= (name, author))

	def onEdit(self, e):
		listBox= self.parent.FindWindowById(self.eventObjectId)
		i= listBox.GetSelection()
		if i!= -1:
			key= self.parent.book_keys[i]
			b= Book.getBookByKey(key)
			Book.remove_book(key)
			self.onAdd(book= b)

	def onRemove(self, e):
		listBox= self.parent.FindWindowById(self.eventObjectId)
		i= listBox.GetSelection()
		if i!= -1:
			key= self.parent.book_keys[i]
			b= Book.getBookByKey(key)
			if gui.messageBox(
			# Translators: Message displayed when trying to remove a book.
			_('Are you sure you want to remove {} by {}?, this can not be undone.').format(b.name, b.author),
			# Translators: Title of message box.
			_('Warning'),
			wx.YES|wx.NO|wx.ICON_QUESTION)== wx.NO:
				return
			Book.remove_book(key)
			sortingFlag= BookDialog.sortByAuthor
			# index of the book to be selected and focused on
			index= i if len(BookDialog.book_keys)>= i+2 else i-1
			self.parent.populateListBox(sortingFlag)
			if index >=0:
				self.parent.focusAndSelect(BookDialog.book_keys[index])
			else:
				self.parent.focusAndSelect()

	def onMoveBook(self, evt, menuItem):
		# menuItem is the menu item or library name that we want to move the book to it.
		listBox= self.parent.FindWindowById(self.eventObjectId)
		i= listBox.GetSelection()
		if i== -1:
			return
		bookKey= self.parent.book_keys[i]
		book= Book.getBookByKey(bookKey)
		# the library to move book to it
		libraryFileName= menuItem+ '.json'
		#log.info(f'libraryFileName: {libraryFileName}')
		# retreaving library data
		try:
			with open(os.path.join(self.parent.libraryDirectory, libraryFileName), encoding= 'utf-8') as f:
				libraryDict= json.load(f)
			if book.key in libraryDict:
				if gui.messageBox(
				# Translators: Message displayed when trying to move a book already present in the other library.
				_("This book is already present in {library} library, under {label} label;\n"
				#" Do you still want to replace it with the one you are about to move?.").format(library= menuItem, label= libraryDict[booklibraryDict[book.key]['label']),
				" Do you still want to replace it with the one you are about to move?.").format(library= menuItem, label= bookKey),
				# Translators: Title of message box.
				_('Warning'),
				wx.YES|wx.NO|wx.ICON_QUESTION)== wx.NO:
					return
			libraryDict[book.key]= {"about": book.about, "size": book.size, "url": book.url, "otherUrls": book.otherUrls}
			with open(os.path.join(self.parent.libraryDirectory, libraryFileName), 'w', encoding= 'utf-8') as f:
				json.dump(libraryDict, f, ensure_ascii= False, indent= 4)
		except Exception as e:
			# Translators: Message displayed when getting an error trying to move a link from one library to another.
			gui.messageBox(_("Unable to move the book to another library"), 
			# Translators: Title of message box
			_("Error"), wx.OK|wx.ICON_ERROR)
			raise e
		else:
			# We have moved the book, now we want to remove it from current library.
			Book.remove_book(book.key)
			# index of the book to be selected and focused on
			index= i if len(self.parent.book_keys)>= i+2 else i-1
			self.parent.populateListBox()
			if index >=0:
				listBox.SetSelection(index)

	def onRemoveAll(self, e):
		if gui.messageBox(
		# Translators: Message displayed when trying to remove all books.
		_('Are you sure you want to remove all books from this library?, this can not be undone.'),
		# Translators: Title of message box.
		_('Warning'),
		wx.YES|wx.NO|wx.ICON_QUESTION)== wx.NO:
			return
		Book.remove_allBooks()
		self.parent.populateListBox()
		self.parent.focusAndSelect()

class BookDialog(wx.Dialog):
	#to insure that there is only one instance of BookDialog class is running
	currentInstance = None
	sortByAuthor= False

	def __init__(self, parent, filename, libraryDirectory, isLocalLibrary: bool):
		super(BookDialog, self).__init__(parent, -1, title= filename, 
		size=(500, 400))
		self.filename= filename
		self.libraryDirectory= libraryDirectory
		self.isLocalLibrary= isLocalLibrary
		#log.info(f'self.isLocalLibrary: {self.isLocalLibrary}')
		Book.saving_dir								= self.libraryDirectory
		#if self.isLocalLibrary:
			# make class attribute for active library.
		BookDialog.activeLibrary= filename
		#sending the filename to the Book class
		Book.filename= filename + ".json"

		panel = wx.Panel(self, -1) 

		listLabel= wx.StaticText(panel, -1, "List Of Books")
		self.listBox= wx.ListBox(panel, -1, style= wx.LB_SINGLE)

		# Translators: Label of about the book text control.
		aboutLabel = wx.StaticText(panel, -1, _("About The Book"))
		self.aboutText = wx.TextCtrl(panel, -1,
			   "Here is a looooooooooooooong line of text set in the control.\n\n"
			   "See that it wrapped, and that this line is after a blank",
			   size=(200, 100), style=wx.TE_MULTILINE|wx.TE_READONLY)

		   # Translators: Label of size of book file text control.
		sizeLabel = wx.StaticText(panel, -1, _("Size of Book:"))
		self.sizeText = wx.TextCtrl(panel, -1, "I've entered some text!", 
				size=(175, -1), style= wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_NO_VSCROLL)

		# Translators: Label of the text control that shows the url .
		urlLabel = wx.StaticText(panel, -1, _("Book Url:"))
		self.urlText = wx.TextCtrl(panel, -1, "http://www.ibra.byethost7.com/main.html", 
		size=(175, -1), style= wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_NO_VSCROLL|wx.TE_PROCESS_ENTER)
		self.urlText.SetSelection(0, -1)

		# Translators: Label of text control that displays the othe urls for the book.
		otherUrlsLabel = wx.StaticText(panel, -1, _("Other Urls for the book:"))
		self.otherUrlsText = wx.TextCtrl(panel, -1, #"http://www.ibra.byethost7.com/main.html",
			   "Here is a looooooooooooooong line of text set in the control.\n\n"
			   "See that it wrapped, and that this line is after a blank",
			   size=(200, 100), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_AUTO_URL|wx.TE_PROCESS_ENTER)
		#size=(175, -1), style= wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_NO_VSCROLL|wx.TE_PROCESS_ENTER)
		#self.anotherUrlText.SetSelection(0, -1)

		# Translators: Label of Access book button.
		self.accessButton= wx.Button(panel, -1, label= _("Access book"))

		#Label of close button.
		self.closeButton= wx.Button(panel, id= wx.ID_CANCEL, label= _("Close"))

		sizer = wx.FlexGridSizer(cols=2, hgap=6, vgap=6)
		sizer.AddMany([listLabel, self.listBox, aboutLabel, self.aboutText, sizeLabel, self.sizeText,urlLabel, self.urlText, otherUrlsLabel, self.otherUrlsText, self.accessButton, self.closeButton])
		panel.SetSizer(sizer)

		#make bindings
		#wx.EVT_CONTEXT_MENU is used in NVDA 2021.1,for wx.EVT_RIGHT_DOWN seized to work.
		self.listBox.Bind(wx.EVT_CONTEXT_MENU, self.OnRightDown)
		self.listBox.Bind(wx.EVT_KILL_FOCUS, self.onKillFocus)
		self.urlText.Bind(wx.EVT_TEXT_ENTER, self.onaccessBook)
		self.otherUrlsText.Bind(wx.EVT_TEXT_ENTER, self.onAnotherUrl)
		self.Bind(wx.EVT_BUTTON, self.onaccessBook, self.accessButton)
		self.Bind(wx.EVT_BUTTON, self.onCancel, self.closeButton)
		self.postInit()

	def postInit(self):
		self.accessButton.SetDefault()
		self.populateListBox()
		self.focusAndSelect()
		self.Raise()
		self.Show()

	def populateListBox(self, sortByAuthor= False):
		Book.retreave_from_file()
		if not Book.myBooks:
			BookDialog.book_keys= []
			self.listBox.Set([])
		else:
			_keys = [eval(k) for k in Book.myBooks]
			if not sortByAuthor:
				BookDialog.book_keys= sorted(_keys)
				# Translators: Phrase to be put between name and author of the book.
				by= _(' by ')
				lst= list(map(lambda x: x[0]+by+x[1] if x[1] else x[0], [key for key in self.book_keys]))
				BookDialog.sortByAuthor= False
			else:
				temp= sorted([(j, i) for i, j in _keys])
				BookDialog.book_keys= [(name, author) for author, name in temp]
				# Translators: Phrase to be put between author and name of the book.
				AinN=_(' in ')
				lst= [x+AinN+y if x else y for x,y in temp]
				BookDialog.sortByAuthor= True
			self.listBox.Set(lst)
		self.numberOfBooks= len(self.book_keys)
		self.SetTitle(u"{}({})".format(self.filename, self.numberOfBooks))

	def focusAndSelect(self, bookKey= None):
		if  self.listBox.IsEmpty():
			self.aboutText.Disable()
			[control.Hide() for control in (self.sizeText, self.urlText, self.otherUrlsText, self.accessButton)]
			self.listBox.SetFocus()
			return
		self.Hide()
		if not bookKey:
			i= 0
		else:
			i= self.book_keys.index(bookKey)
		self.listBox.SetSelection(i)
		key= self.book_keys[i]
		book= Book.getBookByKey(key)
		if book:
			self.showOrHideAboutControl(book.about)
			self.showOrHideControl(self.sizeText, book.size)
			#setting the value of the url control, and show it.
			self.urlText.SetValue(book.url)
			self.urlText.SetSelection(0, -1)
			self.urlText.Show()
			# Show the other urls control if it has a value.
			self.showOrHideControl(self.otherUrlsText, book.otherUrls)
			self.accessButton.Show()
			#self.Hide()
		self.Show()

	def OnRightDown(self, e):
		obj= e.GetEventObject()
		#log.info(f'obj: {obj}')
		id= obj.GetId()
		#log.info(f'objectId: {id}')
		menu= MyPopupMenu(self, id)
		self.PopupMenu(menu, e.GetPosition())
		menu.Destroy()

	def onKillFocus(self, evt):
		#log.info('under kill focus event')
		i= self.listBox.GetSelection()
		#log.info(f'i: {i}')
		if i== -1:
			self.sizeText.Hide()
			self.otherUrlsText.Hide()
		else:
			#log.info(f'self.book_keys: {self.book_keys}')
			book= Book.getBookByKey(self.book_keys[i])
			if book:
				self.showOrHideAboutControl(book.about)
				self.showOrHideControl(self.sizeText, book.size)
				#setting the value of the url control
				self.urlText.SetValue(book.url)
				self.urlText.SetSelection(0, -1)
				#setting the value of the another url
				self.showOrHideControl(self.otherUrlsText, book.otherUrls)
		evt.Skip()

	def showOrHideControl(self, control, value):
		control.SetValue(value)
		if value and not control.IsShown():
			control.Show()
		elif not value and control.IsShown():
			control.Hide()

	def showOrHideAboutControl(self, value):
		if value: # The about text control has some information about the link.
			self.aboutText.SetValue(value)
			self.aboutText.SetSelection(0, -1)
			self.aboutText.Enable()
			#log.info('about is shown')
		else : 
			self.aboutText.Disable()
			#log.info('about is hiddin')

	def onaccessBook(self, evt):
		#log.info('under onDownload handler')
		i= self.listBox.GetSelection()
		if i!= -1:
			try:
				book= Book.getBookByKey(self.book_keys[i])
			except KeyError:
				pass
			else:
				if book.url:
					#webbrowser.open(book.url)
					queueHandler.queueFunction(queueHandler.eventQueue, webbrowser.open, book.url)

	def onAnotherUrl(self, evt):
		focus= api.getFocusObject()
		info1= focus.makeTextInfo('caret')
		info1.expand('line')
		info2= focus.makeTextInfo('all')
		info1.end= info2.end
		text= info1.text
		url= self.getFirstLinkInText(text)
		if url:
			queueHandler.queueFunction(queueHandler.eventQueue, webbrowser.open, url)

	def getFirstLinkInText (self, text):
		"""Find URLs in a text string.
		"""
		import re
		url_re = re.compile(r"(?:https?://|ftp://|www.)[^ ,.?!#%=+][^ ][^ \t\n\r\f\v]*")
		bad_chars = '\'\\.,[](){}:;"'
		links= [s.strip(bad_chars) for s in url_re.findall(text)]
		# remove duplicates
		links= list(dict.fromkeys(links))
		if links:
			return links[0]

	def onCancel(self, evt):
		#log.info('under onCancel') 
		if not self.isLocalLibrary:
			Book.myBooks= {}
		if self.isLocalLibrary and Book.myBooks:
			Book.save_to_file()
		self.Destroy()
"""
	def __del__(self):
		#log.info('under __del__')
		if Book.myBooks:
			Book.save_to_file()
"""