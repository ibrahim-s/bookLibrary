# -*- coding: utf-8 -*-
# Copyright (C) 2025 ibrahim hamadeh, released under GPLv2.0
# onlinebooks.py

import concurrent.futures
import requests
import threading
import json
import tempfile
from pathlib import Path
from logHandler import log

def createTempDir():
	''' Create a directory for online books in %temp% '''
	path = Path(tempfile.gettempdir())/'bookLibrary-online'
	path.mkdir(parents=True, exist_ok=True)
	return path

createdTemporaryDirectory = createTempDir()

thread_local = threading.local()

def get_session():
	if not hasattr(thread_local, "session"):
		thread_local.session = requests.Session()
	return thread_local.session

def download_file(filename):
	#url = 'https://younisyounis.github.io/bookLibraryFiles/'+ filename
	url = 'https://ibrahim-h.github.io/bookLibraryFiles/ar/'+ filename
	filePath = createdTemporaryDirectory/filename
	session = get_session()
	with session.get(url) as response:
		library_dict= response.json()
	with open(filePath, 'w', encoding= 'utf-8') as f:
		json.dump(library_dict, f, ensure_ascii= False, indent= 4)

def download_all_files(files):
	with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
		executor.map(download_file, files)
	#log.info(f'book library files has been downloaded ...')

files= ['الأدب العالمي.json', 'المجموعات القصصية.json']
