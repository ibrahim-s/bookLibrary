# installTasks for bookLibrary
# required to keep or reserve files already present 

import addonHandler
import os
import shutil
import globalVars

def onInstall():
	userPath= os.path.expanduser('~')
	addon_data_path= os.path.join(userPath, "bookLibrary-addonFiles")

	for addon in addonHandler.getAvailableAddons():
		if addon.name == "myArabicLibrary":
			addon.requestRemove()
			# if path exists, so data files are present in it, and only we remove data folder in addon package.
			if os.path.exists(addon_data_path):
				try:
					shutil.rmtree(os.path.join(os.path.dirname(__file__), 'bookLibrary-addonFiles'), ignore_errors=True)
				except:
					pass
				return

			try:
				shutil.copytree(os.path.join(globalVars.appArgs.configPath, "addons", "myArabicLibrary", "mydata"), addon_data_path)
				shutil.rmtree(os.path.join(os.path.dirname(__file__), 'bookLibrary-addonFiles'), ignore_errors=True)
			except:
				pass
			return

	try:
		shutil.copytree(os.path.join(os.path.dirname(__file__), 'bookLibrary-addonFiles'), addon_data_path)
		shutil.rmtree(os.path.join(os.path.dirname(__file__), 'bookLibrary-addonFiles'), ignore_errors=True)
	except Exception as e:
			log.debug('failed to copy or remove data files', exc_info=1)
