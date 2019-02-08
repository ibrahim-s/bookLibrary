# myArabicLibrary 
# required to keep or reserve files already present 
# Borrowed from Golden Cursor addon, thanks to people behind it.

import addonHandler
import os
import shutil

def onInstall():
	oldPath = os.path.join(os.path.dirname(__file__), "..", "myArabicLibrary", "mydata")
	#The new version of the addon will have .pending suffix , and the old one will retain it's name.
	newPath = os.path.join(os.path.dirname(__file__), "mydata")
	if os.path.exists(oldPath):
		try:
			shutil.rmtree(newPath)
			shutil.copytree(oldPath, newPath)
		except (IOError, WindowsError):
			pass
