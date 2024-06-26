# -*- coding: utf-8 -*-
# bookLibrary
# Copyright (C) 2019 ibrahim hamadeh, released under GPLv2.0
# An addon that helps collect and arrange and access easily informations related to a book
# about the book, size of book file, url, and have the ability to download or access the book from the addon.

from globalPluginHandler import GlobalPlugin
import wx, gui
import addonHandler
addonHandler.initTranslation()

from .maindialog import LibraryDialog, LIBRARIES_DIR
MAINDIALOG= None

class GlobalPlugin(GlobalPlugin):
	scriptCategory = _("Book Library")
	def __init__(self):
		super(GlobalPlugin, self).__init__()

	def script_openMyLibrary(self, gesture):
		global MAINDIALOG
		if not MAINDIALOG:
			MAINDIALOG= LibraryDialog(gui.mainFrame, LIBRARIES_DIR)
		else:
			MAINDIALOG.Raise()

	# Translators: message displayed in input help mode for openning  choose library dialog.
	script_openMyLibrary.__doc__ = _('Open Book Library dialog.')

	__gestures = {
		'KB:NVDA+control+windows+b':'openMyLibrary'
	}