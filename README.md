# pyeditor
A python IDE with some features.

V. 0.9.4 - Testing (full usable)

Requires:
- python3
- pyqt5
- qscintilla

This program must be launched by using the bash script pyeditor.sh.

Features:
- word autocompletition
- braces autocompletition
- string/word searching with history of previous searched words
- comment/uncomment, also for a group of line of code
- read only mode
- highlights the selected words by pressing the 'hl' button, and resets by uncheck it
- saves its window size
- file name and path in the titlebar
- load a file if it is passed as argument
- dialogs for loading files or saving the document
- line numbers
- read only or modified tags in the titlebar
- bash scripts support (switching in the gui)
- javascript scripts support (compatible with c, c++, c#, etc.)
- plain text support (no styling at all)
- history of opened files
- zoom (Ctrl+mouse wheel)
- uppercase/lowercase/swapcase in the contextual menu
- wordwrapping
- style colours (almost) fully customizable
- status bar
- optional command line argument: -p for python file, -b for bash file, -j for javascript file, -t for text file (file name is optional) 
- configurable with its config file
- built-in functions: tab/untab, undo/redo (CTRL+z/y), etc.

![My image](https://github.com/frank038/pyeditor/blob/main/image1.png)
