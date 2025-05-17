# Book Library #

Author: Ibrahim Hamadeh  
NVDA compatibility: 2024.1 and later  
Download [version 2.2.5][1]  

This addon helps the user to view and access his downloadable or online books, and for this internet connection is needed.  
At the same time he can arrange his local books in library like way.  
he can add, edit or remove any of his local libraries or books. 

From the main dialog of libraries, you can choose the library you like and press enter on it.  
You can in this dialog, for local libraries, add, Rename or remove any libraries at any time.  
but for online libraries or books, you can't edit that, but you still in the list of online books, you can change sorting of books, by name or Author.
On the library dialog, you can read informations about the books, size of file, the link, and other links if present.  
You can open Book Library dialog pressing on the command: NVDA+control+windows+b  
You can as always change this gesture or command going to :  
NVDA menu>preferences>inputGestures>Book Library.  

## Usage ##

*	First open the main dialog pressing on the default or assigned gesture to the addon.  
*	Two list of libraries , online and local are there
*	choose one of them , then a library from that list, and press enter.  
*	If the list of local libraries is empty, tab and add a library, and Tabing again you can Rename a library or remove it.  
*	Pressing enter on it, a dialog for that library will open, showing all books(title by author) in it in a list .  
*	Tabing on that dialog you can access the about of the book, size, download link, and other links for the book if found.  
*	In case of online books, standing on the list, press the context menu, you then can sort books eithe by name or Author.
*	In case of local books,Stand on the book you want in this dialog, and press the context menu.  
*	From there you can add, edit, remove a book or all.  
*	Moreover, from there you can move book to another library, and sort books, by either title or author.  
*	If you want to access a book with the default or first link, just stand on it and press ente.  
*	If you want to access it with one of the other links, tab to the other links window, stand on the link, and press enter on it.  
*	Lastly do you want to export any library as html or json file, Yes you can  
*	Stand on the library you want to export and press the contact menu, arrow down once to Export library as, choose html or json, and press enter.  
*	A dialog will open to choose the folder you want to export to, choose folder and press enter or navigate to select folder button and press on it.  
*	That's it, an information message will be displayed telling you that the library has been exported, congratulations.  

## online Books ##

You can access online Books or libraries, and for this you need the presence of internet connection.

Go to setting panel for the addon, tab to "choose language of online books" combo box, and select the language you wish.

If some one want to upload collection of libraries in his language, he may do that by creating the libraries in local books region, then navigating to 'home directory/bookLibrary-addonFiles', he will find there the libraries he created in json format,then he may send them to me to finish the job.

### Changes for version 2.2.5 ###

*	Add setting panel, to choose language of online books or libraries. Thus make the possibility to add more books of other languages.

### Changes for version 2.2.4 ###

*	Fix a bug when tabing for first time, and the about of the book is not present, focus goes wrong. Now focus goes right.

### Changes for version 2.2.3 ###

*	Now we have two list of libraries, online and local libraries. 
online libraries are only available for Arabic language  for the time being.

### Changes for version 2.2.2 ###

*	Add Turkish translation, by Umut KORKMAZ.

### Changes for version 2.2.1 ###

*	Now from the main dialog, you can add, Rename or remove any library.
*	Type of data files has been changed from pickle to json.
*	Now url2 control has been fchanged to multi edit control for other links related to the book. 
*	Minumum tested versionis change to 2019.3, dropping support for python2.
*	Last tested version has been updated, making the addon compatible with NVDA 2024.1.

### Changes for version 2.2 ###

*	Update latest tested version to 2021.1  
*	Fix a bug in activating context menu, existed in NVDA 2021.1  

### Changes for version 2.1 ###

*	Added compatibility with python3  

### Changes for version 2.0 ###

*	Rename or change the name of the addon from My Arabic Library to Book Library.  
*	Change the place of addon data files, putting them in the home user directory, after the were in the root directory of the addon.  
Doing that, so that all instances of the book library addon in the installed or portable copy of nvda, can access the same place and use same files.  

### Changes for version 1.1 ###

*	Added export feature to library list, so that you can now export any library as html file.  
*	modifying the sorting feature in book list, showing name and author in a better way.  

### Changes for 1.0 ###

*	Initial version.

### contact me ###

In the case of any bugs or suggestion you can [send me an email.](mailto:ibra.hamadeh@hotmail.com)

[1]: https://github.com/ibrahim-s/bookLibrary/releases/download/v2.2.5/bookLibrary-2.2.5.nvda-addon
