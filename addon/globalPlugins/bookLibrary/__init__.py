# -*- coding: utf-8 -*-
# bookLibrary
# Copyright (C) 2019 ibrahim hamadeh, released under GPLv2.0
# An addon that helps collect and arrange and access easily informations related to a book
# about the book, size of book file, url, and have the ability to download or access the book from the addon.

from globalPluginHandler import GlobalPlugin
from gui import guiHelper
import wx, gui, core
import globalVars, config
import shutil, os
from scriptHandler import script
from .maindialog import LibraryDialog
from.fetchingOnlineData import createdTemporaryDirectory, download_all_files
import addonHandler
addonHandler.initTranslation()

# Available library or book languages
libraryLanguages= [
	('ar', 'Arabic, ar'),
	('tr', 'Turkish, tr')
]

# locals libraries path in home directory
LIBRARIES_DIR= os.path.abspath(os.path.join(os.path.expanduser('~'), 'bookLibrary-addonFiles'))

MAINDIALOG= None

class GlobalPlugin(GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		core.postNvdaStartup.register(self.fetchBooksData)
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(BookLibraryPanel)

	def fetchBooksData(self):
		# Do not fetch data in these conditions.
		if globalVars.appArgs.launcher:
			return
		# starting fetching data process...
		def fetchWithDelay():
			download_all_files()
		wx.CallLater(3000, fetchWithDelay)

	def terminate(self):
		shutil.rmtree(createdTemporaryDirectory, ignore_errors=True)
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(BookLibraryPanel)

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

# Setting panel for book library.
class BookLibraryPanel(gui.settingsDialogs.SettingsPanel):
	# Translators: title of the panel
	title= _("Book Library")

	def makeSettings(self, sizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=sizer)

		languageChoices = [x[1] for x in libraryLanguages]
		self.chooseLanguageCumbo= sHelper.addLabeledControl(
			# Translators: Label of combo box
			_("Choose language for online books:"), wx.Choice, choices= languageChoices)
		self.chooseLanguageCumbo.SetSelection([indx for indx, val in enumerate(libraryLanguages) if val[0]== config.conf["bookLibrary"]["libraryLanguage"]][0])
		#self.chooseLanguageCumbo.SetSelection(config.conf["bookLibrary"]["libraryLanguage"])
		#self.chooseFormCumbo.Bind(wx.EVT_CHOICE, self.onChooseForm)

	def onSave(self):
		config.conf["bookLibrary"]["libraryLanguage"]= [x[0] for x in libraryLanguages][self.chooseLanguageCumbo.GetSelection()]
