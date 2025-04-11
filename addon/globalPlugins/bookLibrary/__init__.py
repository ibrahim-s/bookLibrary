# -*- coding: utf-8 -*-
# bookLibrary
# Copyright (C) 2019 ibrahim hamadeh, released under GPLv2.0
# An addon that helps collect and arrange and access easily informations related to a book
# about the book, size of book file, url, and have the ability to download or access the book from the addon.

from globalPluginHandler import GlobalPlugin
import wx, gui, core
import globalVars
import shutil, os
from scriptHandler import script
from .maindialog import LibraryDialog
from.onlinebooks import createdTemporaryDirectory, download_all_files
import addonHandler
addonHandler.initTranslation()

# locals libraries path in home directory
LIBRARIES_DIR= os.path.abspath(os.path.join(os.path.expanduser('~'), 'bookLibrary-addonFiles'))

MAINDIALOG= None

class GlobalPlugin(GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		core.postNvdaStartup.register(self.fetchBooksData)

	def fetchBooksData(self):
		# Do not fetch data in these conditions.
		if globalVars.appArgs.launcher:
			return
		# starting fetching data process...
		def fetchWithDelay():
			from .onlinebooks import files
			download_all_files(files)
		wx.CallLater(3000, fetchWithDelay)

	def terminate(self):
		shutil.rmtree(createdTemporaryDirectory, ignore_errors=True)

	@script(
		# Translators: Message displayed in input help mode.
		description= _("Open Book Library dialog."),
		gesture= "KB:NVDA+control+windows+b",
		# Translators: Category of addon in input gestures.
		category= _("Book Library")
	)
	def script_openMyLibrary(self, gesture):
		global MAINDIALOG
		if not MAINDIALOG:
			MAINDIALOG= LibraryDialog(gui.mainFrame, LIBRARIES_DIR, createdTemporaryDirectory)
		else:
			MAINDIALOG.Raise()
