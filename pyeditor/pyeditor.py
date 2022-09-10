#!/usr/bin/env python3
# V 0.9.11
import sys
from PyQt5.QtWidgets import (qApp,QMainWindow,QStyleFactory,QWidget,QFileDialog,QSizePolicy,QFrame,QBoxLayout,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QApplication,QDialog,QMessageBox,QLineEdit,QComboBox,QCheckBox,QAction,QMenu,QStatusBar,QTabWidget) 
from PyQt5.QtCore import (Qt,pyqtSignal,QFile,QIODevice,QPoint,QMimeDatabase)
from PyQt5.QtGui import (QColor,QFont,QIcon,QPalette)
from PyQt5.Qsci import (QsciLexerCustom,QsciScintilla,QsciLexerPython,QsciLexerBash,QsciLexerJavaScript)
import os
import re
from cfgpyeditor import *


WINW = 1200
WINH = 600

class firstMessage(QWidget):
    def __init__(self, *args):
        super().__init__()
        title = args[0]
        message = args[1]
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("icons/program.svg"))
        box = QBoxLayout(QBoxLayout.TopToBottom)
        box.setContentsMargins(5,5,5,5)
        self.setLayout(box)
        label = QLabel(message)
        box.addWidget(label)
        button = QPushButton("Close")
        box.addWidget(button)
        button.clicked.connect(self.close)
        self.show()
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
WINM = "False"
if not os.path.exists("pyeditor.cfg"):
    try:
        with open("pyeditor.cfg", "w") as ifile:
            ifile.write("{};{};False".format(WINW, WINH))
    except:
        app = QApplication(sys.argv)
        fm = firstMessage("Error", "The file pyeditor.cfg cannot be created.")
        sys.exit(app.exec_())

if not os.access("pyeditor.cfg", os.R_OK):
    app = QApplication(sys.argv)
    fm = firstMessage("Error", "The file pyeditor.cfg cannot be read.")
    sys.exit(app.exec_())

try:
    with open("pyeditor.cfg", "r") as ifile:
        fcontent = ifile.readline()
    aw, ah, am = fcontent.split(";")
    WINW = aw
    WINH = ah
    WINM = am.strip()
except:
    app = QApplication(sys.argv)
    fm = firstMessage("Error", "The file pyeditor.cfg cannot be read.\nRebuilded.")
    try:
        with open("pyeditor.cfg", "w") as ifile:
            ifile.write("{};{};False".format(WINW, WINH))
    except:
        pass
    sys.exit(app.exec_())
#######################

class textLexer(QsciLexerCustom):
    def __init__(self, __myFont, parent):
        super(textLexer, self).__init__(parent)
        self.__myFont = __myFont
        # Default text settings
        self.setDefaultColor(QColor("#ff000000"))
        self.setDefaultPaper(QColor("#ffffffff"))
        self.setDefaultFont(self.__myFont)
        # Initialize fonts per style
        self.setFont(self.__myFont, 0)
        # Initialize colors per style
        self.setColor(QColor("#ff000000"), 0)   # Style 0: black
        # Initialize paper colors per style
        self.setPaper(QColor("#ffffffff"), 0)   # Style 0: white
    
    def language(self):
        return "TextStyle"
    
    def description(self, style):
        if style == 0:
            return "textStyle"
    
    def styleText(self, start, end):
        self.startStyling(start)
        self.setStyling(end - start, 0)
    
    
class MyQsciScintilla(QsciScintilla):
    keyPressed = pyqtSignal(str)
    def __init__(self):
        super(MyQsciScintilla, self).__init__()
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 1)
        # indicators
        self.indicatorDefine(QsciScintilla.FullBoxIndicator,0, )
        self.setIndicatorForegroundColor(QColor(SELECTIONBACKGROUNDCOLOR), 0)
        self.setIndicatorHoverStyle(QsciScintilla.FullBoxIndicator, 0)
        self.setIndicatorDrawUnder(True, 0)
        self.SendScintilla(QsciScintilla.SCI_SETINDICATORCURRENT, 0)
        self.SendScintilla(QsciScintilla.SCI_SETINDICATORVALUE, 0, 0xffff)
        
        
    def contextMenuEvent(self, e):
        menu = self.createStandardContextMenu()
        if not self.isReadOnly():
            menu.addSeparator()
            #
            customAction1 = QAction("Uppercase")
            customAction1.triggered.connect(self.on_customAction1)
            menu.addAction(customAction1)
            #
            customAction2 = QAction("Lowercase")
            customAction2.triggered.connect(self.on_customAction2)
            menu.addAction(customAction2)
            #
            customAction3 = QAction("Swapcase")
            customAction3.triggered.connect(self.on_customAction3)
            menu.addAction(customAction3)
            # 
            menu.addSeparator()
            #
            customAction4 = QAction("Eol view/hide")
            customAction4.triggered.connect(self.on_customAction4)
            menu.addAction(customAction4)
            #
            customAction5 = QAction("Wordwrap")
            customAction5.triggered.connect(self.on_customAction5)
            menu.addAction(customAction5)
        #
        menu.exec_(e.globalPos()+QPoint(5,5))
        
    def on_customAction1(self):
        if not self.hasSelectedText():
            return
        #
        self.replaceSelectedText(self.selectedText().upper())
        
    def on_customAction2(self):
        if not self.hasSelectedText():
            return
        #
        self.replaceSelectedText(self.selectedText().lower())
        
    def on_customAction3(self):
        if not self.hasSelectedText():
            return
        #
        self.replaceSelectedText(self.selectedText().swapcase())
        
    def on_customAction4(self):
        self.setEolVisibility(not self.eolVisibility())
    
    def on_customAction5(self):
        if self.wrapMode():
            self.setWrapMode(QsciScintilla.WrapNone)
        else:
            self.setWrapMode(QsciScintilla.WrapWord)
    
    def keyPressEvent(self, e):
        QsciScintilla.keyPressEvent(self, e)
        self.keyPressed.emit(e.text())
    
    def mousePressEvent(self, e):
        QsciScintilla.mousePressEvent(self, e)
        self.keyPressed.emit(None)
        

class CustomMainWindow(QMainWindow):
    def __init__(self):
        super(CustomMainWindow, self).__init__()
        self.setContentsMargins(0,0,0,0)
        self.setWindowIcon(QIcon("icons/program.svg"))
        self.resize(int(WINW), int(WINH))
        self.setWindowTitle("pyeditor")
        # Create frame and layout
        # ---------------------------
        #
        self.__frm = QFrame(self)
        self.__frm.setContentsMargins(0,0,0,0)
        # self.__frm.setStyleSheet("QWidget { background-color: #ffeaeaea }")
        self.__lyt = QVBoxLayout()
        self.__lyt.setContentsMargins(2,2,2,2)
        self.__frm.setLayout(self.__lyt)
        self.setCentralWidget(self.__frm)
        # ------------------
        self.btn_box0 = QHBoxLayout()
        self.__lyt.addLayout(self.btn_box0)
        #
        self.btn_h = QPushButton("H")
        self.btn_h.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.btn_box0.addWidget(self.btn_h, alignment=Qt.AlignLeft)
        self.btn_h_menu = QMenu()
        self.btn_h.setMenu(self.btn_h_menu)
        self.btn_h_menu.triggered.connect(self.on_h_menu)
        #
        self.btn_new = QPushButton("New")
        self.btn_new.clicked.connect(self.on_new)
        self.btn_box0.addWidget(self.btn_new, stretch=1)
        #
        self.btn_open = QPushButton("Open")
        self.btn_open.clicked.connect(self.on_open)
        self.btn_box0.addWidget(self.btn_open, stretch=1)
        #
        self.__btn = QPushButton("Exit")
        self.__btn.clicked.connect(self.__btn_action)
        self.btn_box0.addWidget(self.__btn, stretch=1)
        # the history of opened files
        self.pageNameHistory = []
        try:
            if not os.path.exists("pyeditorh.txt"):
                ff = open("pyeditorh.txt", "w")
                ff.close()
            #
            with open("pyeditorh.txt", "r") as ff:
                self.pageNameHistory = ff.readlines()
        except Exception as E:
            MyDialog("Error", str(E)+"\nExiting...", self)
            self.close()
            sys.exit()
        #
        self.pageName = ""
        afilename = ""
        if len(sys.argv) > 1:
            if sys.argv[1] in ["-p", "-b", "-j", "-t"]:
                if len(sys.argv) > 2:
                    afilename = os.path.realpath(sys.argv[2])
            else:
                afilename = os.path.realpath(sys.argv[1])
        #
        # for el in self.pageNameHistory[::-1]:
        for el in self.pageNameHistory:
            if el.rstrip("\n") == self.pageName:
                continue
            self.btn_h_menu.addAction(el.rstrip("\n"))
        #
        # if self.pageName:
        if afilename:
            # populate the menu - opened doc at last position
            # save into the list once
            if afilename+"\n" in self.pageNameHistory:
                self.pageNameHistory.remove(afilename+"\n")
            else:
                self.btn_h_menu.addAction(afilename)
            self.pageNameHistory.append(afilename+"\n")
        #########
        ### tabwidget
        self.frmtab = QTabWidget()
        self.frmtab.setContentsMargins(0,0,0,0)
        self.__lyt.addWidget(self.frmtab)
        self.frmtab.setTabPosition(3)
        self.frmtab.setTabBarAutoHide(False)
        # self.frmtab.setTabsClosable(True)
        self.frmtab.setMovable(True)
        # self.frmtab.tabCloseRequested.connect(self.on_tab_close)
        self.frmtab.currentChanged.connect(self.on_tab_changed)
        #
        # set the default editor style from command line
        self.isargument = 4
        use_mimetype = 1
        if len(sys.argv) > 1:
            if sys.argv[1] == "-p":
                self.isargument = 1
                use_mimetype = 0
            elif sys.argv[1] == "-b":
                self.isargument = 2
                use_mimetype = 0
            elif sys.argv[1] == "-j":
                self.isargument = 3
                use_mimetype = 0
            elif sys.argv[1] == "-t":
                self.isargument = 4
                use_mimetype = 0
        # or from config file
        if self.isargument == 0:
            if EDITORTYPE == "python":
                self.isargument = 1
                use_mimetype = 0
            elif EDITORTYPE == "bash":
                self.isargument = 2
                use_mimetype = 0
            elif EDITORTYPE == "javascript":
                self.isargument = 3
                use_mimetype = 0
            elif EDITORTYPE == "text":
                self.isargument = 4
                use_mimetype = 0
        # check from the mimetype of the file
        if use_mimetype:
            file_type = QMimeDatabase().mimeTypeForFile(afilename, QMimeDatabase.MatchDefault).name()
            if file_type == "text/x-python3" or file_type == "text/x-python":
                self.isargument = 1
            elif file_type == "application/x-shellscript":
                self.isargument = 2
            elif file_type == "application/javascript":
                self.isargument = 3
            elif file_type == "text/plain":
                self.isargument = 4
        # 
        pop_tab = ftab(afilename, self.isargument, self)
        self.frmtab.addTab(pop_tab, os.path.basename(afilename) or "Unknown")
        self.frmtab.setTabToolTip(0, afilename or "Unknown")
        if afilename:
            if not os.access(afilename, os.W_OK):
                self.frmtab.tabBar().setTabTextColor(self.frmtab.count()-1, QColor("#009900"))
        #
        self.setWindowTitle("pyeditor - {}".format(os.path.basename(afilename) or "Unknown"))
        #
        self.show()
        
    def on_tab_changed(self, idx):
        # self.sender().tabText(idx)
        self.setWindowTitle("pyeditor - {}".format(self.frmtab.tabText(idx)))
    
    # open a file from the history
    def on_h_menu(self, action):
        fileName = action.text()
        #
        is_found = 0
        for tt in range(self.frmtab.count()):
            if self.frmtab.tabText(tt) == os.path.basename(fileName.strip("\n")):
                is_found = 1
                break
        if is_found:
            MyDialog("Info", "File already opened.", self)
        else:
            self.on_open_f(fileName.strip("\n"))
        
    def on_new(self):
        ret = retDialogBox("Question", "Create a new document?", self)
        if ret.getValue() == 0:
            return
        #
        fileName = ""
        pop_tab = ftab(fileName, self.isargument, self)
        self.frmtab.addTab(pop_tab, os.path.basename(fileName) or "Unknown")
        self.frmtab.setTabToolTip(0, fileName or "Unknown")
        self.frmtab.setCurrentIndex(self.frmtab.count()-1)
    
    def on_open(self):
        ret = retDialogBox("Question", "Open a new document?", self)
        if ret.getValue() == 0:
            return
        #
        fileName, _ = QFileDialog.getOpenFileName(self, "Select the file", os.path.expanduser('~'), "All Files (*)")
        if fileName:
            if os.path.exists(fileName) and os.path.isfile(fileName) and os.access(fileName, os.R_OK):
                self.on_open_f(fileName)
            else:
                MyDialog("Error", "Problem with the file.\nIt doesn't exist or it isn't readable.", self)
        
    # related to on_open
    def on_open_f(self, fileName):
        if fileName:
            if not os.path.isfile(fileName):
                MyDialog("Info", "Not a file.", self)
                return
            #
            pop_tab = ftab(fileName, self.isargument, self)
            self.frmtab.addTab(pop_tab, os.path.basename(fileName) or "Unknown")
            self.frmtab.setTabToolTip(0, fileName or "Unknown")
            self.frmtab.setCurrentIndex(self.frmtab.count()-1)
            #
            if not os.access(fileName, os.W_OK):
                self.frmtab.tabBar().setTabTextColor(self.frmtab.count()-1, QColor("#009900"))
            #
            if not fileName+"\n" in self.pageNameHistory:
                self.btn_h_menu.addAction(fileName)
                self.pageNameHistory.append(fileName+"\n")
    
    def __btn_action(self):
        self.close()
    
    def closeEvent(self, event):
        isModified = False
        #
        for tt in range(self.frmtab.count()):
            if self.frmtab.widget(tt).isModified:
                isModified = True
                break
        #
        if isModified:
            ret = retDialogBox("Question", "This document has been modified. \nDo you want to proceed anyway?", self)
            if ret.getValue() == 0:
                event.ignore()
                return
        #
        else:
            ret = retDialogBox("Question", "Exit?", self)
            if ret.getValue() == 0:
                event.ignore()
                return
        # 
        self.on_close()
        
    def on_close(self):
        # save the history
        try:
            with open("pyeditorh.txt", "w") as ff:
                for el in self.pageNameHistory[-HISTORYLIMIT:]:
                    ff.write(el)
        except Exception as E:
            MyDialog("Error", "Cannot save the file history.", self)
        #
        new_w = self.size().width()
        new_h = self.size().height()
        if new_w != int(WINW) or new_h != int(WINH):
            # WINW = width
            # WINH = height
            # WINM = maximized
            isMaximized = self.isMaximized()
            # close without update the file
            if isMaximized == True:
                qApp.quit()
                return
            #
            try:
                ifile = open("pyeditor.cfg", "w")
                ifile.write("{};{};False".format(new_w, new_h))
                ifile.close()
            except Exception as E:
                MyDialog("Error", str(E), self)
        qApp.quit()
    
    # #
    # def on_tab_close(self, idx):
        # if self.frmtab.widget(idx).isModified:
            # MyDialog("Info", "Save the file first.", self)
            # return
        # else:
            # if self.frmtab.count() > 1:
                # self.frmtab.removeTab(idx)
                # return
            # self.on_open_f("")
    
    
class ftab(QWidget):
    def __init__(self, afilename, editortype, parent):
        super().__init__()
        self.parent = parent
        self.setContentsMargins(1,1,1,1)
        self.isargument = editortype
        self.isModified = False
        # default font
        self.__myFont = QFont()
        self.__myFont.setFamily(FONTFAMILY)
        self.__myFont.setPointSize(FONTSIZE)
        #
        # default bold font
        self.__myFontB = QFont()
        self.__myFontB.setFamily(FONTFAMILY)
        self.__myFontB.setPointSize(FONTSIZE)
        self.__myFontB.setWeight(QFont.Bold)
        #
        self.pageName = None
        if afilename:
            filePath = os.path.realpath(afilename)
            if os.path.exists(filePath) and os.path.isfile(filePath) and os.access(filePath, os.R_OK):
                self.pageName = filePath
        #
        self.his_searched = []
        #
        self.search_is_open = 0
        #
        self.sufftype = ""
        #
        self.pop_tab(afilename)
    
    def __is_modified(self):
        return self.isModified
    
    def pop_tab(self, afilename):
        self.__lyt = QVBoxLayout()
        self.__lyt.setContentsMargins(1,1,1,1)
        self.setLayout(self.__lyt)
        # document buttons
        self.btn_box = QHBoxLayout()
        self.__lyt.addLayout(self.btn_box)
        #
        self.combo_tab = QComboBox()
        self.combo_tab.addItems(["Spaces", "Tab"])
        self.btn_box.addWidget(self.combo_tab)
        #
        self.combo_space = QComboBox()
        self.combo_space.addItems(["2","3","4","5","6","7","8"])
        self.btn_box.addWidget(self.combo_space)
        #
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["p", "b", "j", "t"])
        self.btn_box.addWidget(self.lang_combo)
        #
        # self.combo_eol = QComboBox()
        # self.combo_eol.addItems(["L","W"])
        # self.btn_box.addWidget(self.combo_eol)
        #
        self.btn_ro = QPushButton("RO")
        self.btn_ro.clicked.connect(self.on_read_only)
        self.btn_box.addWidget(self.btn_ro, stretch=1)
        #  
        self.btn_save = QPushButton("Save")
        self.btn_save.clicked.connect(self.on_save)
        self.btn_box.addWidget(self.btn_save, stretch=1)
        #
        self.btn_save_as = QPushButton("Save as...")
        self.btn_save_as.clicked.connect(self.on_save_as)
        self.btn_box.addWidget(self.btn_save_as, stretch=1)
        #
        self.__btn_close = QPushButton("Close")
        self.__btn_close.clicked.connect(self.__btn_action_close)
        self.btn_box.addWidget(self.__btn_close, stretch=1)
        #
        self.btn_search = QPushButton("Search")
        self.btn_search.clicked.connect(self.on_search)
        self.btn_box.addWidget(self.btn_search, stretch=1)
        #
        self.btn_comment = QPushButton("Comm")
        self.btn_comment.clicked.connect(self.on_btn_comment)
        self.btn_box.addWidget(self.btn_comment, stretch=1)
        #
        self.btn_uncomment = QPushButton("Uncomm")
        self.btn_uncomment.clicked.connect(self.on_btn_uncomment)
        self.btn_box.addWidget(self.btn_uncomment, stretch=1)
        #
        self.btn_hl = QPushButton("hl")
        self.btn_hl.setCheckable(True)
        self.btn_hl.clicked.connect(self.on_btn_hl)
        self.btn_box.addWidget(self.btn_hl, stretch=0)
        # ----------------------------------------
        # self.__editor = QsciScintilla()
        self.__editor = MyQsciScintilla()
        # load the file passed as argument
        filenotfound = 0
        try:
            if self.pageName and os.path.exists(self.pageName) and os.path.isfile(self.pageName) and os.access(self.pageName, os.R_OK):
                fd = QFile(self.pageName)
                fd.open(QIODevice.ReadOnly)
                self.__editor.read(fd)
                fd.close()
            else:
                filenotfound = 1
        except Exception as E:
            MyDialog("Error", str(E), self)
        #
        self.__editor.setLexer(None)            # We install lexer later
        self.__editor.setUtf8(True)             # Set encoding to UTF-8
        # Brace matchingself.frmtab.
        self.__editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        #####
        self.__editor.setAutoCompletionThreshold(AUTOCOMPLETITION_CHARS)
        self.__editor.setAutoCompletionCaseSensitivity(True)
        self.__editor.setAutoCompletionReplaceWord(False)
        self.__editor.setAutoCompletionUseSingle(QsciScintilla.AcusNever)
        self.__editor.autoCompleteFromDocument()
        self.__editor.setAutoCompletionSource(QsciScintilla.AcsDocument)
        if USEWORDAUTOCOMLETION:
            self.__editor.setAutoCompletionWordSeparators(["."])
        # # End-of-line mode
        # # --------------------
        # if ENDOFLINE == "unix":
            # self.__editor.setEolMode(QsciScintilla.EolUnix)
        # elif ENDOFLINE == "windows":
            # self.__editor.setEolMode(QsciScintilla.EolWindows)
            # self.combo_eol.setCurrentIndex(1)
        #
        self.__editor.setEolVisibility(False)
        # Indentation
        # ---------------
        self.__editor.setIndentationsUseTabs(USETAB)
        self.__editor.setTabWidth(TABWIDTH)
        self.combo_tab.currentIndexChanged.connect(self.on_combo_tab)
        self.combo_tab.setCurrentIndex(USETAB)
        self.combo_space.currentIndexChanged.connect(self.on_combo_space)
        self.combo_space.setCurrentIndex(max(TABWIDTH, 2)-2)
        # self.combo_eol.currentIndexChanged.connect(self.on_eol)
        self.__editor.setIndentationGuides(True)
        self.__editor.setTabIndents(True)
        self.__editor.setAutoIndent(True)
        self.__editor.setBackspaceUnindents(True)
        # a character has been typed
        # self.__editor.SCN_CHARADDED.connect(filenotfoundself.on_k)
        self.__editor.keyPressed.connect(self.on_k)
        # the text has been modified
        self.__editor.modificationChanged.connect(self.on_text_changed)
        # Caret
        # ---------
        self.__editor.setCaretLineVisible(True)
        self.__editor.setCaretWidth(CARETWIDTH)
        # Margins
        # -----------
        # Margin 0 = Line nr margin
        self.__editor.setMarginType(0, QsciScintilla.NumberMargin)
        self.__editor.setMarginWidth(0, "00000")
        #######################
        # # self.__lexer = MyLexer(self.__editor)
        # self.__lexer = QsciLexerPython(self.__editor)
        self.__lexer = textLexer(self.__myFont, self.__editor)
        self.__lexer.setDefaultFont(self.__myFont)
        self.__editor.setLexer(self.__lexer)
        #
        # font
        self.__lexer.setFont(QFont(FONTFAMILY, FONTSIZE))
        ##################
        # 
        # ! Add editor to layout !
        # -------------------------
        self.__lyt.addWidget(self.__editor, stretch=1)
        # 
        self.__editor.setContextMenuPolicy(Qt.DefaultContextMenu)
        #
        # python
        if self.isargument == 1:
            self.lang_combo.setCurrentIndex(0)
            self.on_lang_combo(0)
            self.lpython()
        # bash
        elif self.isargument == 2:
            self.lang_combo.setCurrentIndex(1)
            self.on_lang_combo(1)
            self.lbash()
        # javascript
        elif self.isargument == 3:
            self.lang_combo.setCurrentIndex(2)
            self.on_lang_combo(2)
            self.ljavascript()
        # text
        elif self.isargument == 4:
            self.lang_combo.setCurrentIndex(3)
            self.on_lang_combo(3)
            self.ltext()
        #
        if STATUSBAR:
            self.statusBar = QStatusBar()
            self.__lyt.addWidget(self.statusBar)
            self.statusBar.showMessage("line: {0}/{1} column: {2}".format("-", "-", "-"))
        # set the theme colours
        self.on_theme()
        #
        self.lang_combo.currentIndexChanged.connect(self.on_lang_combo)
        #
        self.show()
        # 
        if filenotfound and afilename:
            MyDialog("Error", "The file\n\n{}\n\ndoesn't exist or it isn't readable.".format(afilename), self)
        # file is not writable
        if self.pageName and not os.access(self.pageName, os.W_OK):
            self.__editor.setReadOnly(True)
            self.btn_ro.setStyleSheet("QPushButton {color: #009900;}")
            #
            self.combo_tab.setEnabled(False)
            self.combo_space.setEnabled(False)
            self.lang_combo.setEnabled(False)
            self.btn_save.setEnabled(False)
            self.btn_save_as.setEnabled(False)
            self.btn_comment.setEnabled(False)
            self.btn_uncomment.setEnabled(False)
            self.btn_hl.setEnabled(False)
        
    def on_btn_hl(self):
        if self.btn_hl.isChecked():
            if self.__editor.hasSelectedText():
                htext = self.__editor.selectedText()
                #
                lines = self.__editor.lines()
                #
                for line in range(lines):
                    ret = [m.start() for m in re.finditer(htext, self.__editor.text(line))]
                    # 
                    if ret:
                        self.__editor.fillIndicatorRange(     
                        line, # line from
                        ret[0], # column from
                        line, # line to
                        ret[0]+len(htext), # column to
                        0 )
        else:
            lines = self.__editor.lines()
            for line in range(lines):
                self.__editor.clearIndicatorRange(line, 0, line, len(self.__editor.text(line)), 0)
    
    def on_combo_tab(self, idx):
        self.__editor.setIndentationsUseTabs(bool(idx))
        if idx:
            self.combo_space.setEnabled(False)
        else:
            self.combo_space.setEnabled(True)
        
    def on_combo_space(self, idx):
        self.__editor.setTabWidth(int(idx)+2)
    
    # def on_eol(self, idx):
        # self.combo_eol.setCurrentIndex(idx)
    
    def on_theme(self):
        if DARKTHEME:
            self.__editor.setMarginsForegroundColor(QColor(DMARGINFOREGROUND))
            self.__editor.setMarginsBackgroundColor(QColor(DMARGINBACKGROUND))
            self.__editor.setMarginsFont(self.__myFont)
            # Caret
            self.__editor.setCaretForegroundColor(QColor(DCARETFORE))
            self.__editor.setCaretLineBackgroundColor(QColor(DCARETBACK))
        else:
            self.__editor.setMarginsForegroundColor(QColor(MARGINFOREGROUND))
            self.__editor.setMarginsBackgroundColor(QColor(MARGINBACKGROUND))
            self.__editor.setMarginsFont(self.__myFont)
            # Caret
            self.__editor.setCaretForegroundColor(QColor(CARETFORE))
            self.__editor.setCaretLineBackgroundColor(QColor(CARETBACK))
            #
        # editor background color
        if DARKTHEME:
            self.__lexer.setPaper(QColor(DEDITORBACKCOLOR))
        else:
            self.__lexer.setPaper(QColor(EDITORBACKCOLOR))
        # Brace matching
        if DARKTHEME:
            self.__editor.setMatchedBraceBackgroundColor(QColor(DMATCHEDBRACECOLOR))
            # selected word colour
            self.__editor.setSelectionBackgroundColor(QColor(DSELECTIONBACKGROUNDCOLOR))
        else:
            self.__editor.setMatchedBraceBackgroundColor(QColor(MATCHEDBRACECOLOR))
            # selected word colour
            self.__editor.setSelectionBackgroundColor(QColor(SELECTIONBACKGROUNDCOLOR))
    
    def on_text_changed(self):
        self.isModified = True
        curr_idx = self.parent.frmtab.currentIndex()
        self.parent.frmtab.tabBar().setTabTextColor(curr_idx, Qt.red)
    
    def lpython(self):
        if not CUSTOMCOLORS:
            return
        if DARKTHEME:
            # Default
            self.__lexer.setColor(QColor(PDDEFAULT), 0)
            # Comment
            self.__lexer.setFont(self.__myFont, 1)
            self.__lexer.setColor(QColor(PDCOMMENT), 1)
            # Number
            self.__lexer.setColor(QColor(PDNUMBER), 2)
            # Double-quoted string
            self.__lexer.setFont(self.__myFont, 3)
            self.__lexer.setColor(QColor(PDDOUBLEQ), 3)
            # Single-quoted string
            self.__lexer.setFont(self.__myFont, 4)
            self.__lexer.setColor(QColor(PDSINGELQ), 4)
            # Keyw1ord
            self.__lexer.setFont(self.__myFontB, 5)
            self.__lexer.setColor(QColor(PDKEYW), 5)
            # Triple single-quoted string
            self.__lexer.setColor(QColor(PDTRIPLESQ), 6)
            # Triple double-quoted string
            self.__lexer.setColor(QColor(PDTRIPLEDQ), 7)
            # Class name
            self.__lexer.setFont(self.__myFontB, 8)
            self.__lexer.setColor(QColor(PDCLASSNAME), 8)
            # Function or method name
            self.__lexer.setColor(QColor(PDFUNCTION), 9)
            # Operator
            self.__lexer.setColor(QColor(PDOPERATOR), 10)
            # Identifier
            self.__lexer.setColor(QColor(PDIDENTIFIER), 11)
            # Comment block
            self.__lexer.setColor(QColor(PDCOMMENTB), 12)
            # Unclosed string
            self.__lexer.setColor(QColor(PDUNCLOSEDSTRING), 13)
            # Highlighted identifier
            self.__lexer.setColor(QColor(PDHIGHLIGHTED), 14)
            # Decorator
            self.__lexer.setFont(self.__myFontB, 15)
            self.__lexer.setColor(QColor(PDDECORATOR), 15)
        else:
            # Default
            self.__lexer.setColor(QColor(PDEFAULT), 0)
            # Comment
            self.__lexer.setFont(self.__myFont, 1)
            self.__lexer.setColor(QColor(PCOMMENT), 1)
            # Number
            self.__lexer.setColor(QColor(PNUMBER), 2)
            # Double-quoted string
            self.__lexer.setFont(self.__myFont, 3)
            self.__lexer.setColor(QColor(PDOUBLEQ), 3)
            # Single-quoted string
            self.__lexer.setFont(self.__myFont, 4)
            self.__lexer.setColor(QColor(PSINGELQ), 4)
            # Keyword
            self.__lexer.setFont(self.__myFontB, 5)
            self.__lexer.setColor(QColor(PKEYW), 5)
            # Triple single-quoted string
            self.__lexer.setColor(QColor(PTRIPLESQ), 6)
            # Triple double-quoted string
            self.__lexer.setColor(QColor(PTRIPLEDQ), 7)
            # Class name
            self.__lexer.setFont(self.__myFontB, 8)
            self.__lexer.setColor(QColor(PCLASSNAME), 8)
            # Function or method name
            self.__lexer.setColor(QColor(PFUNCTION), 9)
            # Operator
            self.__lexer.setColor(QColor(POPERATOR), 10)
            # Identifier
            self.__lexer.setColor(QColor(PIDENTIFIER), 11)
            # Comment block
            self.__lexer.setColor(QColor(PCOMMENTB), 12)
            # Unclosed string
            self.__lexer.setColor(QColor(PUNCLOSEDSTRING), 13)
            # Highlighted identifier
            self.__lexer.setColor(QColor(PHIGHLIGHTED), 14)
            # Decorator
            self.__lexer.setFont(self.__myFontB, 15)
            self.__lexer.setColor(QColor(PDECORATOR), 15)
    
    def lbash(self):
        if not CUSTOMCOLORS:
            return
        if DARKTHEME:
            # Default
            self.__lexer.setColor(QColor(BDDEFAULT), 0)
            # Error
            self.__lexer.setColor(QColor(BDERROR), 1)
            # Comment
            self.__lexer.setFont(self.__myFont, 2)
            self.__lexer.setColor(QColor(BDCOMMENT), 2)
            # Number
            self.__lexer.setColor(QColor(BDNUMBER), 3)
            # Keyword
            self.__lexer.setFont(self.__myFontB, 4)
            self.__lexer.setColor(QColor(BDKEYW), 4)
            # Double-quoted string
            self.__lexer.setFont(self.__myFont, 5)
            self.__lexer.setColor(QColor(BDDOUBLEQ), 5)
            # Single-quoted string
            self.__lexer.setFont(self.__myFont, 6)
            self.__lexer.setColor(QColor(BDSINGELQ), 6)
            # Operator
            self.__lexer.setColor(QColor(BDOPERATOR), 7)
            # Identifier
            self.__lexer.setColor(QColor(BDIDENTIFIER), 8)
            # Scalar
            self.__lexer.setColor(QColor(BDSCALAR), 9)
            # Parameter expansion
            self.__lexer.setColor(QColor(BDPAREXP), 10)
            # Backticks
            self.__lexer.setColor(QColor(BDBACKTICK), 11)
            # Here document delimiter
            self.__lexer.setColor(QColor(BDHDOCDEL), 12)
            # Single-quoted here document
            self.__lexer.setColor(QColor(BDSQHEREDOC), 13)
        else:
            # Default
            self.__lexer.setColor(QColor(BDEFAULT), 0)
            # Error
            self.__lexer.setColor(QColor(BERROR), 1)
            # Comment
            self.__lexer.setFont(self.__myFont, 2)
            self.__lexer.setColor(QColor(BCOMMENT), 2)
            # Number
            self.__lexer.setColor(QColor(BNUMBER), 3)
            # Keyword
            self.__lexer.setFont(self.__myFontB, 4)
            self.__lexer.setColor(QColor(BKEYW), 4)
            # Double-quoted string
            self.__lexer.setFont(self.__myFont, 5)
            self.__lexer.setColor(QColor(BDOUBLEQ), 5)
            # Single-quoted string
            self.__lexer.setFont(self.__myFont, 6)
            self.__lexer.setColor(QColor(BSINGELQ), 6)
            # Operator
            self.__lexer.setColor(QColor(BOPERATOR), 7)
            # Identifier
            self.__lexer.setColor(QColor(BIDENTIFIER), 8)
            # Scalar
            self.__lexer.setColor(QColor(BSCALAR), 9)
            # Parameter expansion
            self.__lexer.setColor(QColor(BPAREXP), 10)
            # Backticks
            self.__lexer.setColor(QColor(BBACKTICK), 11)
            # Here document delimiter
            self.__lexer.setColor(QColor(BHDOCDEL), 12)
            # Single-quoted here document
            self.__lexer.setColor(QColor(BSQHEREDOC), 13)
    
    def ljavascript(self):
        if not CUSTOMCOLORS:
            return
        if DARKTHEME:
            # Default
            self.__lexer.setColor(QColor(JDDEFAULT), 0)
            # C comment
            # C++ comment
            # JavaDoc style C comment
            # JavaDoc style pre-processor comment
            # JavaDoc style C++ co    mment
            # Pre-processor C comment
            # JavaDoc style pre-processor comment
            self.__lexer.setFont(self.__myFont, 1)
            self.__lexer.setColor(QColor(JDCOMMENT), 1)
            self.__lexer.setFont(self.__myFont, 2)
            self.__lexer.setColor(QColor(JDCOMMENT), 2)
            self.__lexer.setFont(self.__myFont, 3)
            self.__lexer.setColor(QColor(JDCOMMENT), 3)
            self.__lexer.setFont(self.__myFont, 15)
            self.__lexer.setColor(QColor(JDCOMMENT), 15)
            self.__lexer.setColor(QColor(JDCOMMENT), 23)
            self.__lexer.setColor(QColor(JDCOMMENT), 24)
            # Number
            self.__lexer.setColor(QColor(JDNUMBER), 4)
            # Keyword
            # JavaDoc keyword
            self.__lexer.setFont(self.__myFontB, 5)
            self.__lexer.setColor(QColor(JDKEYW), 5)
            self.__lexer.setFont(self.__myFontB, 17)
            self.__lexer.setColor(QColor(JDKEYW), 17)
            # Double-quoted string
            self.__lexer.setFont(self.__myFont, 6)
            self.__lexer.setColor(QColor(JDDOUBLEQ), 6)
            # Single-quoted string
            self.__lexer.setFont(self.__myFont, 7)
            self.__lexer.setColor(QColor(JDSINGELQ), 7)
            # IDL UUID
            self.__lexer.setColor(QColor(JDUUID), 8)
            # Pre-processor block
            self.__lexer.setColor(QColor(JDPREPB), 9)
            # Operator
            self.__lexer.setColor(QColor(JDOPERATOR), 10)
            # Identifier
            self.__lexer.setColor(QColor(JDIDENTIFIER), 11)
            # Unclosed string
            self.__lexer.setColor(QColor(JDUNCLOSEDS), 12)
            # C# verbatim string
            self.__lexer.setColor(QColor(JDCVERBS), 13)
            # Regular expression
            self.__lexer.setColor(QColor(JDREGESPR), 14)
            # Secondary keywords and identifiers
            self.__lexer.setColor(QColor(JDSECKI), 16)
            # JavaDoc keyword error
            self.__lexer.setColor(QColor(JDJAVADOCERROR), 18)
            # Global classes and typedefs
            self.__lexer.setFont(self.__myFontB, 19)
            self.__lexer.setColor(QColor(JDCLASSES), 19)
            # C++ raw string
            self.__lexer.setColor(QColor(JDDEFAULT), 20)
            # Vala triple-quoted verbatim string
            self.__lexer.setColor(QColor(JDDEFAULT), 21)
            # Pike hash-quoted string
            self.__lexer.setColor(QColor(JDPIKEHQS), 22)
            # User-defined literal
            self.__lexer.setColor(QColor(JDUSERDLIT), 25)
            # Task marker
            self.__lexer.setColor(QColor(JDTASKMARKER), 26)
            # Escape sequence
            self.__lexer.setColor(QColor(JDESCAPES), 27)
        else:
            # Default
            self.__lexer.setColor(QColor(JDEFAULT), 0)
            # C comment
            # C++ comment
            # JavaDoc style C comment
            # JavaDoc style pre-processor comment
            # JavaDoc style C++ comment
            # Pre-processor C comment
            # JavaDoc style pre-processor comment
            self.__lexer.setFont(self.__myFont, 1)
            self.__lexer.setColor(QColor(JCOMMENT), 1)
            self.__lexer.setFont(self.__myFont, 2)
            self.__lexer.setColor(QColor(JCOMMENT), 2)
            self.__lexer.setFont(self.__myFont, 3)
            self.__lexer.setColor(QColor(JCOMMENT), 3)
            self.__lexer.setFont(self.__myFont, 15)
            self.__lexer.setColor(QColor(JCOMMENT), 15)
            self.__lexer.setColor(QColor(JCOMMENT), 23)
            self.__lexer.setColor(QColor(JCOMMENT), 24)
            # Number
            self.__lexer.setColor(QColor(JNUMBER), 4)
            # Keyword
            # JavaDoc keyword
            self.__lexer.setFont(self.__myFontB, 5)
            self.__lexer.setColor(QColor(JKEYW), 5)
            self.__lexer.setFont(self.__myFontB, 17)
            self.__lexer.setColor(QColor(JKEYW), 17)
            # Double-quoted string
            self.__lexer.setFont(self.__myFont, 6)
            self.__lexer.setColor(QColor(JDOUBLEQ), 6)
            # Single-quoted string
            self.__lexer.setFont(self.__myFont, 7)
            self.__lexer.setColor(QColor(JSINGELQ), 7)
            # IDL UUID
            self.__lexer.setColor(QColor(JUUID), 8)
            # Pre-processor block
            self.__lexer.setColor(QColor(JPREPB), 9)
            # Operator
            self.__lexer.setColor(QColor(JOPERATOR), 10)
            # Identifier
            self.__lexer.setColor(QColor(JIDENTIFIER), 11)
            # Unclosed string
            self.__lexer.setColor(QColor(JUNCLOSEDS), 12)
            # C# verbatim string
            self.__lexer.setColor(QColor(JCVERBS), 13)
            # Regular expression
            self.__lexer.setColor(QColor(JREGESPR), 14)
            # Secondary keywords and identifiers
            self.__lexer.setColor(QColor(JSECKI), 16)
            # JavaDoc keyword error
            self.__lexer.setColor(QColor(JJAVADOCERROR), 18)
            # Global classes and typedefs
            self.__lexer.setFont(self.__myFontB, 19)
            self.__lexer.setColor(QColor(JCLASSES), 19)
            # C++ raw string
            self.__lexer.setColor(QColor(JDEFAULT), 20)
            # Vala triple-quoted verbatim string
            self.__lexer.setColor(QColor(JDEFAULT), 21)
            # Pike hash-quoted string
            self.__lexer.setColor(QColor(JPIKEHQS), 22)
            # User-defined literal
            self.__lexer.setColor(QColor(JUSERDLIT), 25)
            # Task marker
            self.__lexer.setColor(QColor(JTASKMARKER), 26)
            # Escape sequence
            self.__lexer.setColor(QColor(JESCAPES), 27)
    
    def ltext(self):
        if DARKTHEME:
            # Default
            self.__lexer.setColor(QColor(PDDEFAULT), 0)
        else:
            # Default
            self.__lexer.setColor(QColor(PDEFAULT), 0)
    
    #
    def on_lang_combo(self, idx):
        if idx == 0:
            self.STRCOMM = "# "
            self.sufftype = ".py"
            self.__lexer = QsciLexerPython(self.__editor)
            self.__lexer.setDefaultFont(self.__myFont)
            self.__editor.setLexer(self.__lexer)
            #
            self.__editor.setAutoCompletionCaseSensitivity(True)
            # set the styles
            self.lpython()
            # set the theme colours
            self.on_theme()
        elif idx == 1:
            self.STRCOMM = "# "
            self.sufftype = ".sh"
            self.__lexer = QsciLexerBash(self.__editor)
            self.__lexer.setDefaultFont(self.__myFont)
            self.__editor.setLexer(self.__lexer)
            #
            self.__editor.setAutoCompletionCaseSensitivity(True)
            # set the styles
            self.lbash()
            # set the theme colours
            self.on_theme()
        elif idx == 2:
            self.STRCOMM = "// "
            self.sufftype = ".js"
            self.__lexer = QsciLexerJavaScript(self.__editor)
            self.__lexer.setDefaultFont(self.__myFont)
            self.__editor.setLexer(self.__lexer)
            # 
            self.__editor.setAutoCompletionCaseSensitivity(True)
            # set the styles
            self.ljavascript()
            # set the theme colours
            self.on_theme()
        elif idx == 3:
            self.STRCOMM = "// "
            self.sufftype = ".txt"
            self.__lexer = textLexer(self.__myFont, self.__editor)
            self.__editor.setLexer(self.__lexer)
            self.__editor.setAutoCompletionCaseSensitivity(True)
            self.ltext()
            # set the theme colours
            self.on_theme()
    
    #
    def on_read_only(self):
        if self.isModified:
            MyDialog("Info", "Save this document first.", self)
            return
        #
        if self.pageName:
            if not os.access(self.pageName, os.W_OK):
                MyDialog("Info", "This document cannot be written.", self)
                return
        #
        if not self.__editor.isReadOnly():
            self.__editor.setReadOnly(True)
            self.sender().setStyleSheet("QPushButton {color: #009900;}")
            curr_idx = self.parent.frmtab.currentIndex()
            self.parent.frmtab.tabBar().setTabTextColor(curr_idx, QColor("#009900"))
            self.combo_tab.setEnabled(False)
            self.combo_space.setEnabled(False)
            self.lang_combo.setEnabled(False)
            self.btn_save.setEnabled(False)
            self.btn_save_as.setEnabled(False)
            self.btn_comment.setEnabled(False)
            self.btn_uncomment.setEnabled(False)
            self.btn_hl.setEnabled(False)
        else:
            self.__editor.setReadOnly(False)
            self.sender().setStyleSheet("")
            curr_idx = self.parent.frmtab.currentIndex()
            self.parent.frmtab.tabBar().setTabTextColor(curr_idx, QColor(QPalette.Text))
            self.combo_tab.setEnabled(True)
            self.combo_space.setEnabled(True)
            self.lang_combo.setEnabled(True)
            self.btn_save.setEnabled(True)
            self.btn_save_as.setEnabled(True)
            self.btn_comment.setEnabled(True)
            self.btn_uncomment.setEnabled(True)
            self.btn_hl.setEnabled(True)
    
    #
    def on_save_as(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "File Name...", os.path.join(os.path.expanduser("~"), self.pageName or "document{}".format(self.sufftype)), "All Files (*)")
        if fileName:
            self.pageName = fileName
            self.on_save()
    
    #
    def on_save(self):
        if not self.pageName:
            self.pageName = os.path.join(os.path.expanduser("~"), "document{}".format(self.sufftype))
            self.on_save_as()
            return
        #
        issaved = 0
        try:
            fd = QFile(self.pageName)
            fd.open(QIODevice.WriteOnly)
            ret = self.__editor.write(fd)
            issaved = ret
            fd.close()
        except Exception as E:
            MyDialog("Error", str(E), self)
        #
        if issaved:
            self.isModified = False
            #
            if not self.pageName+"\n" in self.parent.pageNameHistory:
                self.parent.btn_h_menu.addAction(self.pageName+"\n")
                self.parent.pageNameHistory.append(self.pageName+"\n")
            curr_idx = self.parent.frmtab.currentIndex()
            # # the file is only saved with a new name - it will not used
            # if not self.pageName:
            self.parent.frmtab.setTabText(curr_idx, os.path.basename(self.pageName))
            self.parent.frmtab.setTabToolTip(curr_idx, self.pageName)
            curr_idx = self.parent.frmtab.currentIndex()
            self.parent.frmtab.tabBar().setTabTextColor(curr_idx, QColor(QPalette.Text))
            # self.parent.frmtab.tabBar().setTabTextColor(curr_idx, Qt.green)
        else:
            MyDialog("Error", "Problem while saving the file.", self)
        
    #
    def on_search(self):
        if self.search_is_open:
            return
        ret_text = self.__editor.selectedText()
        ret = searchDialog(self, ret_text, self.__editor)
    
    #
    def on_btn_comment(self):
        if self.__editor.isReadOnly():
            return
        #
        line_from, _, line_to, _ = self.__editor.getSelection()
        # lines selected
        if line_from != -1 and line_to != -1:
            for line in range(line_from, line_to + 1):
                if self.__editor.text(line) == "":
                    continue
                #
                i = 0
                while self.__editor.text(line)[i] == " " or self.__editor.text(line)[i] == "\t":
                    i += 1
                #
                self.__editor.insertAt(self.STRCOMM, line, i)
        # no selection
        else:
            line, idx = self.__editor.getCursorPosition()
            if self.__editor.text(line) == "":
                return
            #
            i = 0
            while self.__editor.text(line)[i] == " " or self.__editor.text(line)[i] == "\t":
                i += 1
            #
            self.__editor.insertAt(self.STRCOMM, line, i)
    
    #
    def on_btn_uncomment(self):
        if self.__editor.isReadOnly():
            return
        #
        line_from, _, line_to, _ = self.__editor.getSelection()
        # lines selected
        if line_from != -1 and line_to != -1:
            for line in range(line_from, line_to + 1):
                if self.__editor.text(line) == "":
                    continue
                #
                i = 0
                while self.__editor.text(line)[i] == " " or self.__editor.text(line)[i] == "\t":
                    i += 1
                if self.__editor.text(line)[i:i+len(self.STRCOMM)] == self.STRCOMM:
                    self.__editor.setCursorPosition(line, i)
                    self.__editor.setSelection(line, i, line, i+len(self.STRCOMM))
                    self.__editor.removeSelectedText()
        # no selection
        else:
            line, idx = self.__editor.getCursorPosition()
            if self.__editor.text(line) == "":
                return
            #
            i = 0
            while self.__editor.text(line)[i] == " " or self.__editor.text(line)[i] == "\t":
                i += 1
            #
            if self.__editor.text(line)[i:i+len(self.STRCOMM)] == self.STRCOMM:
                self.__editor.setCursorPosition(line, i)
                self.__editor.setSelection(line, i, line, i+len(self.STRCOMM))
                self.__editor.removeSelectedText()
    
    
    # insert a character if a certain one has been typed
    def on_k(self, id):
        if self.__editor.isReadOnly():
            return
        # 40 ( - 39 ' - 34 " - 91 [ - 123 {
        if AUTOCLOSE:
            # if id == 40:
            if id == "(":
                self.__editor.insert(")")
            # elif id == 39:
            elif id == "'":
                self.__editor.insert("'")
            # elif id == 34:
            elif id == '"':
                self.__editor.insert('"')
            # elif id == 91:
            elif id == "[":
                self.__editor.insert(']')
            # elif id == 123:
            elif id == "{":
                self.__editor.insert('}')
        #
        if STATUSBAR:
            line, column = self.__editor.getCursorPosition()
            lines = self.__editor.lines()
            self.statusBar.showMessage("line: {0}/{1} column: {2}".format(line+1, lines, column))
        # the document has been modified
        if not self.isModified:
            if id == '':
                return
            self.isModified = True
            curr_idx = self.parent.frmtab.currentIndex()
            self.parent.frmtab.tabBar().setTabTextColor(curr_idx, Qt.red)
    
    def wheelEvent(self, e):
        if e.modifiers() & Qt.CTRL:
            if e.angleDelta().y() < 0:
                self.__editor.zoomOut()
            else:
                self.__editor.zoomIn()
    
    def __btn_action_close(self):
        if self.isModified:
            ret = retDialogBox("Question", "This document has been modified. \nDo you want to proceed anyway?", self)
            if ret.getValue() == 0:
                return
        #
        else:
            ret = retDialogBox("Question", "Close this document?", self)
            if ret.getValue() == 0:
                return
        #
        if self.parent.frmtab.count() > 1:
            curr_idx = self.parent.frmtab.currentIndex()
            self.parent.frmtab.removeTab(curr_idx)
            return
        else:
            self.__editor.setText("")
            self.isModified = False
            curr_idx = self.parent.frmtab.currentIndex()
            self.parent.frmtab.setTabText(curr_idx, "Unknown")
            self.parent.frmtab.tabBar().setTabTextColor(curr_idx, QColor(QPalette.Text))
            self.parent.setWindowTitle("pyeditor - Unknown")
            self.statusBar.showMessage("line: -/- column: -")

# simple dialog message
# type - message - parent
class MyDialog(QMessageBox):
    def __init__(self, *args):
        super(MyDialog, self).__init__(args[-1])
        if args[0] == "Info":
            self.setIcon(QMessageBox.Information)
            self.setStandardButtons(QMessageBox.Ok)
        elif args[0] == "Error":
            self.setIcon(QMessageBox.Critical)
            self.setStandardButtons(QMessageBox.Ok)
        elif args[0] == "Question":
            self.setIcon(QMessageBox.Question)
            self.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)
        self.setWindowIcon(QIcon("icons/program.svg"))
        self.setWindowTitle(args[0])
        self.resize(DIALOGWIDTH,300)
        self.setText(args[1])
        retval = self.exec_()
    
    # def event(self, e):
        # result = QMessageBox.event(self, e)
        # #
        # self.setMinimumHeight(0)
        # self.setMaximumHeight(16777215)
        # self.setMinimumWidth(0)
        # self.setMaximumWidth(16777215)
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # # 
        # return result

class searchDialog(QDialog):
    def __init__(self, parent, ret_text, editor):
        super(searchDialog, self).__init__(parent)
        self.parent = parent
        self.editor = editor
        # this dialog is open
        self.parent.search_is_open = 1
        self.setWindowIcon(QIcon("icons/program.svg"))
        self.setWindowTitle("Search...")
        # self.setWindowModality(Qt.ApplicationModal)
        self.resize(DIALOGWIDTH, 300)
        #
        vbox = QBoxLayout(QBoxLayout.TopToBottom)
        vbox.setContentsMargins(5,5,5,5)
        self.setLayout(vbox)
        #
        # self.line_edit = QLineEdit()
        self.line_edit = QComboBox()
        self.line_edit.setEditable(True)
        if ret_text and len(ret_text) < 35:
            # self.line_edit.setText(ret_text)
            if ret_text in self.parent.his_searched:
                self.parent.his_searched.remove(ret_text)
            self.parent.his_searched.insert(0, ret_text)
        self.line_edit.addItems(self.parent.his_searched)
        #
        vbox.addWidget(self.line_edit)
        #
        self.chk_sens = QCheckBox("Case sensitive")
        vbox.addWidget(self.chk_sens)
        #
        self.chk_word = QCheckBox("Word matching")
        vbox.addWidget(self.chk_word)
        #
        self.chk = QCheckBox("Substitutions")
        self.chk.stateChanged.connect(self.on_chk)
        vbox.addWidget(self.chk)
        #
        self.line_edit_sub = QLineEdit()
        self.line_edit_sub.setEnabled(False)
        self.line_edit.currentTextChanged.connect(self.le_cur_changed)
        vbox.addWidget(self.line_edit_sub)
        ### button box
        hbox = QBoxLayout(QBoxLayout.LeftToRight)
        vbox.addLayout(hbox)
        #
        self.button4 = QPushButton("Previous")
        self.button4.clicked.connect(lambda:self.on_find(0))
        hbox.addWidget(self.button4)
        #
        self.button2 = QPushButton("Next")
        self.button2.clicked.connect(lambda:self.on_find(1))
        hbox.addWidget(self.button2)
        #
        button3 = QPushButton("Close")
        button3.clicked.connect(self.close_)
        hbox.addWidget(button3)
        #
        self.first_found = False
        self.isForward = True
        #
        self.Value = 0
        #
        # self.exec_()
        self.show()
        
    def le_cur_changed(self, new_text):
        self.first_found = False
    
    def on_find(self, ftype):
        line_edit_text = self.line_edit.currentText()
        if line_edit_text == "":
            return
        #
        if not line_edit_text in self.parent.his_searched:
            self.parent.his_searched.insert(0, line_edit_text)
        # substitutions
        if ftype and self.chk.isChecked():
            pline, pcol = self.editor.getCursorPosition()
            ret = self.editor.findFirst(line_edit_text, False, self.chk_sens.isChecked(), self.chk_word.isChecked(), False, True, 0, 0, False)
            while ret:
                self.editor.replace(self.line_edit_sub.text())
                ret = self.editor.findNext()
            # else:
                # self.editor.cancelFind()
            #
            self.editor.setCursorPosition(pline, pcol)
            #
            return
        #
        # if ftype == 1 and self.isForward == False: 
            # self.first_found = False
        # elif ftype == 0 and self.isForward == True:
            # self.first_found = False
        #
        if ftype:
            # if not self.first_found:
            if not self.first_found or not self.isForward:
                self.isForward = True
                ret = self.editor.findFirst(line_edit_text, False, self.chk_sens.isChecked(), self.chk_word.isChecked(), False, True)
                self.first_found = ret
            else:
                self.editor.findNext()
        else:
            # if not self.first_found:
            if not self.first_found or self.isForward:
                self.isForward = False
                ret = self.editor.findFirst(line_edit_text, False, self.chk_sens.isChecked(), self.chk_word.isChecked(), False, False)
                self.first_found = ret
            else:
                self.editor.findNext()
        
    def on_chk(self, idx):
        if idx:
            self.line_edit_sub.setEnabled(True)
            self.button4.setEnabled(False)
            self.setWindowTitle("Replace")
            self.button2.setText("Find all")
        else:
            self.line_edit_sub.setEnabled(False)
            self.button4.setEnabled(True)
            self.setWindowTitle("Search...")
            self.button2.setText("Next")
        
    
    def getValue(self):
        return self.Value
    
    def close_(self):
        self.parent.search_is_open = 0
        self.close()


# dialog - return of the choise yes or no
class retDialogBox(QMessageBox):
    def __init__(self, *args):
        super(retDialogBox, self).__init__(args[-1])
        self.setWindowIcon(QIcon("icons/program.svg"))
        self.setWindowTitle(args[0])
        if args[0] == "Info":
            self.setIcon(QMessageBox.Information)
        elif args[0] == "Error":
            self.setIcon(QMessageBox.Critical)
        elif args[0] == "Question":
            self.setIcon(QMessageBox.Question)
        self.resize(DIALOGWIDTH, 100)
        self.setText(args[1])
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        #
        self.Value = None
        retval = self.exec_()
        #
        if retval == QMessageBox.Yes:
            self.Value = 1
        elif retval == QMessageBox.Cancel:
            self.Value = 0
    
    def getValue(self):
        return self.Value
    
    # def event(self, e):
        # result = QMessageBox.event(self, e)
        # #
        # self.setMinimumHeight(0)
        # self.setMaximumHeight(16777215)
        # self.setMinimumWidth(0)
        # self.setMaximumWidth(16777215)
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # #
        # textEdit = self.findChild(QTextEdit)
        # if textEdit != None :
            # textEdit.setMinimumHeight(0)
            # textEdit.setMaximumHeight(16777215)
            # textEdit.setMinimumWidth(0)
            # textEdit.setMaximumWidth(16777215)
            # textEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # #
        # return result
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    if GUISTYLE:
        QApplication.setStyle(QStyleFactory.create(GUISTYLE))
    # Now use a palette to switch to dark colors
    if DARKTHEME:
        # TEXTCOLOR = QColor("#C5C8C6")
        TEXTCOLOR = QColor("#969896")
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, TEXTCOLOR)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.black)
        palette.setColor(QPalette.ToolTipText, TEXTCOLOR)
        palette.setColor(QPalette.Text, TEXTCOLOR)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, TEXTCOLOR)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(palette)
    #
    myGUI = CustomMainWindow()
    sys.exit(app.exec_())
    
########################
