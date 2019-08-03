# -*- coding: utf-8 -*-
#bookdialog.py
#graphical user interface for book dialog

import wx, gui
import webbrowser
import queueHandler
from .books import Book
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
	#return result

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
	if result:
		b= Book.getBookByUrl(result)
		if b:
			gui.messageBox(
			# Translators: message displayed when the url is present for another book.
			_('This url is present for book {} by {}; please enter another one').format(b.name, b.author), 
			_('Warning'))
			return getBookUrl(message, caption, book)
	return result

def getBookUrl2(message, caption, book= None):
	dlg= wx.TextEntryDialog(None, message, caption)
	if book:
		dlg.SetValue(book.url2)
	dlg.ShowModal()
	result= dlg.GetValue().strip()
	if result:
		b= Book.getBookByUrl2(result)
		if b:
			gui.messageBox(
			# Translators: message displayed when url2 is present for another book.
			_('This url is present for book {} by {}; please enter another one').format(b.name, b.author), 
			_('Warning'))
			return getBookUrl2(message, caption, book)
	return result

#the popup menu class
class MyPopupMenu(wx.Menu):
	def __init__(self, parent, eventObjectId):
		super(MyPopupMenu, self).__init__()
        
		self.parent = parent
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

		#Remove All Books menu
		removeAll= wx.MenuItem(self, -1, 
		# Translators: label of menu items to remove all books.
		_('Remove All '))
		self.Append(removeAll)
		self.Bind(wx.EVT_MENU, self.onRemoveAll, removeAll)

	def onSortByAuthor(self, evt):
		#if self.sortByName.IsChecked():
		if not BookDialog.sortByAuthor:
			self.parent.populateListBox(sortByAuthor=True)
			self.parent.focusAndSelect()
			BookDialog.sortByAuthor= True
		else: pass

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
		if (name, author) in Book.myBooks:
			gui.messageBox('This book already exist in library, please enter a new one or remove existed first', 'Warning')
			return
		#getting the about of the book
		about= getBookAbout(_("Write Something About The Book"), 
		_("About"), book)
		#getting size of book
		size= getBookSize(_("Enter Size of Book or file"), 
		_("size"), book)
		#log.info('size: %s'%size)

		#getting the url of the book
		url= getBookUrl(_('Enter Url source to download book file(www...)'), 
		_('Url:'), book)
		#log.info('url: %s'%url)

		#getting url2
		url2= getBookUrl2(_('Enter another url if present, or leave blank'), 
		_('Another url:'), book)
		Book.add_book(name, author, about, size, url, url2)
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
			self.parent.populateListBox(sortingFlag)
			self.parent.focusAndSelect()

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
	sortByAuthor= False
	#to insure that there is only one instance of BookDialog class is running
	BOOKDIALOG= None

	def __init__(self, parent, filename):
		super(BookDialog, self).__init__(parent, -1, title= filename, 
		size=(500, 300))
		self.filename= filename
		#sending the filename to the Book class
		#Book.filename= u"%s"%filename + u".pickle"
		Book.filename= filename + ".pickle"

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
		urlLabel = wx.StaticText(panel, -1, _("Url:"))
		self.urlText = wx.TextCtrl(panel, -1, "http://www.ibra.byethost7.com/main.html", 
		size=(175, -1), style= wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_NO_VSCROLL|wx.TE_PROCESS_ENTER)
		self.urlText.SetSelection(0, -1)

		# Translators: Label of text control that displays the another url.
		anotherUrlLabel = wx.StaticText(panel, -1, _("Another Url:"))
		self.anotherUrlText = wx.TextCtrl(panel, -1, "http://www.ibra.byethost7.com/main.html",
		size=(175, -1), style= wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_NO_VSCROLL|wx.TE_PROCESS_ENTER)
		#self.anotherUrlText.SetSelection(0, -1)

		# Translators: Label of download file button.
		self.downloadButton= wx.Button(panel, -1, label= _("Download File"))
		#Label of Cancel button.
		self.cancelButton= wx.Button(panel, id= wx.ID_CANCEL, label= _("Cancel"))

		sizer = wx.FlexGridSizer(cols=2, hgap=6, vgap=6)
		sizer.AddMany([listLabel, self.listBox, aboutLabel, self.aboutText, sizeLabel, self.sizeText,urlLabel, self.urlText, anotherUrlLabel, self.anotherUrlText, self.downloadButton, self.cancelButton])
		panel.SetSizer(sizer)

		#make bindings
		self.listBox.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
		self.listBox.Bind(wx.EVT_KILL_FOCUS, self.onKillFocus)
		self.urlText.Bind(wx.EVT_TEXT_ENTER, self.onDownload)
		self.anotherUrlText.Bind(wx.EVT_TEXT_ENTER, self.onAnotherUrl)
		self.Bind(wx.EVT_BUTTON, self.onDownload, self.downloadButton)
		self.Bind(wx.EVT_BUTTON, self.onCancel, self.cancelButton)
		self.postInit()

	def postInit(self):
		self.downloadButton.SetDefault()
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
			_keys = [k for k in Book.myBooks]
			if not sortByAuthor:
				BookDialog.book_keys= sorted(_keys)
				#lst= [key[0]+' by '+key[1] for key in self.book_keys]
				lst= map(lambda x: x[0]+ u' تأليف '+x[1] if x[1] else x[0], [key for key in self.book_keys])
			else:
				temp= sorted([(j, i) for i, j in _keys])
				BookDialog.book_keys= [(name, author) for author, name in temp]
				#lst= [author+'; '+name for author, name in temp]
				lst= map(lambda (x,y): x+u' في '+y if x else y, temp)
			self.listBox.Set(lst)
		self.numberOfBooks= len(self.book_keys)
		self.SetTitle(u"{}({})".format(self.filename, self.numberOfBooks))

	def focusAndSelect(self, bookKey= None):
		if  self.listBox.IsEmpty():
			self.listBox.SetFocus()
			return
		if not bookKey:
			self.listBox.SetSelection(0)
			#self.listBox.SetFocus()
		else:
			i= self.book_keys.index(bookKey)
			self.listBox.SetSelection(i)
			#self.listBox.SetFocus()
			self.Hide()
			self.Show()

	def OnRightDown(self, e):
#		print 'hi'
		obj= e.GetEventObject()
		id= obj.GetId()
		self.PopupMenu(MyPopupMenu(self, id), e.GetPosition())

	def onKillFocus(self, evt):
		#log.info('under kill focus event')
		i= self.listBox.GetSelection()
		if i== -1:
			self.sizeText.Hide()
			self.anotherUrlText.Hide()
		else:
			try:
				book= Book.getBookByKey(self.book_keys[i])
			except KeyError:
				pass
			else:
				#setting the value of the about control
				self.aboutText.SetValue(book.about)
				self.aboutText.SetSelection(0, -1)
				#setting the value of the size control
				self.showOrHideControl(self.sizeText, book.size)
				#setting the value of the url control
				self.urlText.SetValue(book.url)
				self.urlText.SetSelection(0, -1)
				#setting the value of the another url
				self.showOrHideControl(self.anotherUrlText, book.url2)
		evt.Skip()

	def showOrHideControl(self, control, value):
		control.SetValue(value)
		if control== self.anotherUrlText:
			control.SetSelection(0, -1)
		if value and not control.IsShown():
			control.Show()
		elif not value and control.IsShown():
			control.Hide()

	def onDownload(self, evt):
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
		url= self.anotherUrlText.GetValue()
		if url:
			queueHandler.queueFunction(queueHandler.eventQueue, webbrowser.open, url)

	def onCancel(self, evt):
		#log.info('under onCancel') 
		if Book.myBooks:
			Book.save_to_file()
		self.Destroy()
"""
	def __del__(self):
		#log.info('under __del__')
		if Book.myBooks:
			Book.save_to_file()
"""
if __name__ == '__main__':
	app = wx.App()
	frame = BookDialog(None, 'hello')
	frame.postInit()
	app.MainLoop()
