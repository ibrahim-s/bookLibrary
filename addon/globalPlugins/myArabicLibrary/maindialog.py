# -*- coding: utf-8 -*-
# maindialog.py
#graphical user interface for the list of libraries.

#for compatibility with python3
try:
	import cPickle as pickle
except ImportError:
	import pickle

import wx, gui, ui
import core
import os
import codecs
from logHandler import log
from .books import Book
from .bookdialog import BookDialog

import addonHandler
addonHandler.initTranslation()

CURRENT_DIR= os.path.dirname(os.path.abspath(__file__))
LIBRARIES_DIR= os.path.abspath(os.path.join(CURRENT_DIR,'..', '..', 'mydata')).decode("mbcs")

def makeHtmlFile(libraryName, libraryData, newpath):
	''' Make Html file out of pickle library file.'''
	with codecs.open(newpath, 'wb', encoding= 'utf-8') as html:
		html.write(u"""<!DOCTYPE html><html lang="en"><head>
			<meta charset="UTF-8">
<title>{} </title>
		</head><body>
		<h1>{}</h1>
		<ol>""".format(u'مكتبتي العربية', libraryName)
		)
		for name, author, about, size, url, url2 in libraryData:
			html.write(u'<li><h2>{} {}</h2>'.format(name, u' تأليف '+author if author else author))
			html.write(u'<p>Download Url:</p>')
			html.write(u'<p><a href= "{}">{}</a></p>'.format('http://'+url if url.startswith('www.') else url, name))
			if url2:
				html.write(u'<p><a href= "{}">Another Link</a></p>'.format('http://'+url2 if url2.startswith('www.') else url2))
			if size:
				html.write(u'<p>Size: {}</p>'.format(size))
			if about:
				html.write(u"<h3>{}</h3><p>{}</p>".format(u'عن الكتاب', about))
			html.write(u'</li>')
		html.write(u'</ol></body></html>')
		return True

class LibraryPopupMenu(wx.Menu):
	''' The menu that pops up upon right clicking on the list box or list of libraries.'''
	def __init__(self, parent, objectId):
		super(LibraryPopupMenu, self).__init__()
        
		self.parent = parent
		self.objectId= objectId

		#Add export Library as html menu.
		exportHtml= wx.MenuItem(self, wx.ID_ANY, 
		# Translators: label obj menu items to export a library as html.
		_('Export Library as html'))
		self.Append(exportHtml)
		self.Bind(wx.EVT_MENU, self.onExportHtml, exportHtml)

	def onExportHtml(self, evt):
		library_name= self.parent.FindWindowById(self.objectId).GetStringSelection()
		path= os.path.join(LIBRARIES_DIR, library_name+'.pickle')
		try:
			with open(path, 'rb') as f:
				d= pickle.load(f)
		except EOFError:
			gui.messageBox(
			_('Failed to open library, or may be library selected is empty.'),
			# Translators:title of message dialog
			_('Error'), wx.OK|wx.ICON_ERROR)
			return
		else:
			#the library data as list of tuple of six items  (name, author, about, size, url, url2), which are the attributes of a book.
			library_data= sorted([(key[0], key[1], d[key]['about'], d[key]['size'], d[key]['url'], d[key]['url2']) for key in d])#, key= lambda x: x[1])

		dlg = wx.DirDialog(self.parent, "Choose a directory:",
		style=wx.DD_DEFAULT_STYLE
| wx.DD_DIR_MUST_EXIST
		)
		if dlg.ShowModal() == wx.ID_OK:
			path_chosen= dlg.GetPath()
			log.info(path_chosen)
		dlg.Destroy()
		if path_chosen:
			html_path= os.path.join(path_chosen, library_name+ '.html')
			try:
				makeHtmlFile(library_name, library_data, html_path)
			except Exception as e:
				wx.CallAfter(gui.messageBox,
				# Translators: message of error dialog displayed when cannot export library file.
				_("Failed to export library"),
				# Translators: title of error dialog .
				_("Error"),
				wx.OK|wx.ICON_ERROR)
				raise e
			else:
				core.callLater(200, ui.message,
				# Translators: Message presented when library has been exported.
				_("Information: Library Exported"))
				

class ChooseLibrary(wx.Dialog):
	def __init__(self, parent):
		super(ChooseLibrary, self).__init__(parent, title= u'مكتبتي العربية')
		#self.libraryFiles= libraryFiles

		panel= wx.Panel(self)
		mainSizer=wx.BoxSizer(wx.HORIZONTAL)
		listBoxSizer= wx.BoxSizer(wx.VERTICAL)
		staticText= wx.StaticText(panel, -1, u'إختر مكتبة لو سمحت')
		self.listBox = wx.ListBox(panel,-1, style= wx.LB_SINGLE)
		self.listBox.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
		listBoxSizer.Add(staticText, 0, wx.ALL, 5)
		listBoxSizer.Add(self.listBox, 1, wx.ALL|wx.EXPAND, 5)
		mainSizer.Add(listBoxSizer, 1, wx.ALL, 5)

		buttonSizer= wx.BoxSizer(wx.VERTICAL)
		self.ok= wx.Button(panel, wx.ID_OK, _('OK'))
		self.ok.SetDefault()
		self.ok.Bind(wx.EVT_BUTTON, self.onOk)
		buttonSizer.Add(self.ok, 1,wx.ALL, 10)
		self.cancel = wx.Button(panel, wx.ID_CANCEL, _('cancel'))
		self.cancel.Bind(wx.EVT_BUTTON, self.onCancel)
		buttonSizer.Add(self.cancel, 0, wx.EXPAND|wx.ALL, 10)
		mainSizer.Add(buttonSizer, 0, wx.EXPAND|wx.ALL, 5)
		panel.SetSizer(mainSizer)
		self.postInit()

	def postInit(self):
		foundFiles= os.listdir(os.path.join(CURRENT_DIR,'..', '..', 'mydata'))
		libraryFiles= sorted([os.path.splitext(f)[0].decode("mbcs") for f in foundFiles])
		self.libraryFiles= libraryFiles
		self.listBox.Set(libraryFiles)
		self.listBox.SetSelection(0)
		self.Raise()
		self.Show()

	def OnRightDown(self, e):
		log.info('under right down handler') 
		obj= e.GetEventObject()
		id= obj.GetId()
		self.PopupMenu(LibraryPopupMenu(self, id), e.GetPosition())

	def onOk(self, evt):
		i= self.listBox.GetSelection()
		if i != -1:
			filename= self.libraryFiles[i]
			#dlg= BookDialog(gui.mainFrame, filename)
			if  BookDialog.BOOKDIALOG:
				gui.messageBox(
				# Translators: Message be displayed when a library dialog is already opened.
			_('A library dialog is already opened; Close it first please.'),
			# Translators: Title of dialog.
			_('information'))
				return
			else:
				wx.CallAfter(self.openBookDialog, filename)
			self.Destroy()
		

	def openBookDialog(self, filename):
		#global bookDialog
		bookDialog= BookDialog(gui.mainFrame, filename)
		BookDialog.BOOKDIALOG= bookDialog

	def onCancel(self, e):
		self.Destroy()

if __name__== '__main__':
	x= wx.App()
	ChooseLibrary(None)
	x.MainLoop()