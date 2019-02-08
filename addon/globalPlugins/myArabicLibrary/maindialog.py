# -*- coding: utf-8 -*-
#graphical user interface

import wx, gui
import os
from .books import Book
from .bookdialog import BookDialog

import addonHandler
addonHandler.initTranslation()

CURRENT_DIR= os.path.dirname(os.path.abspath(__file__))

class ChooseLibrary(wx.Dialog):
	def __init__(self, parent):
		super(ChooseLibrary, self).__init__(parent, title= u'مكتبتي العربية')
		#self.libraryFiles= libraryFiles

		panel= wx.Panel(self)
		mainSizer=wx.BoxSizer(wx.HORIZONTAL)
		listBoxSizer= wx.BoxSizer(wx.VERTICAL)
		staticText= wx.StaticText(panel, -1, u'إختر مكتبة لو سمحت')
		self.listBox = wx.ListBox(panel,-1, style= wx.LB_SINGLE)
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
		libraryFiles= [os.path.splitext(f)[0].decode("mbcs") for f in foundFiles]
		self.libraryFiles= libraryFiles
		self.listBox.Set(libraryFiles)
		self.listBox.SetSelection(0)
#		self.ok.SetDefault()
		self.Raise()
		self.Show()

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