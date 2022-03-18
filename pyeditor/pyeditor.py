#!/usr/bin/env python3
# V 0.4.2
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qsci import *
import os
from cfgpyeditor import *


WINW = 1500
WINH = 900

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

class MyQsciScintilla(QsciScintilla):
    def __init__(self):
        super(MyQsciScintilla, self).__init__()
    
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
        menu.exec_(e.globalPos())
        
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
    

class CustomMainWindow(QMainWindow):
    def __init__(self):
        super(CustomMainWindow, self).__init__()
        self.setWindowIcon(QIcon("icons/progam.png"))
        self.resize(int(WINW), int(WINH))
        #
        # has been modified
        self.isModified = False
        # Create frame and layout
        # ---------------------------
        self.__frm = QFrame(self)
        # self.__frm.setStyleSheet("QWidget { background-color: #ffeaeaea }")
        self.__lyt = QVBoxLayout()
        self.__frm.setLayout(self.__lyt)
        self.setCentralWidget(self.__frm)
        self.__myFont = QFont()
        self.__myFont.setFamily(FONTFAMILY)
        self.__myFont.setPointSize(FONTSIZE)
        #
        # ------------------
        self.btn_box0 = QHBoxLayout()
        self.__lyt.addLayout(self.btn_box0)
        #
        self.btn_h = QPushButton("H")
        self.btn_h.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.btn_box0.addWidget(self.btn_h)
        self.btn_h_menu = QMenu()
        self.btn_h.setMenu(self.btn_h_menu)
        self.btn_h_menu.triggered.connect(self.on_h_menu)
        #
        self.btn_new = QPushButton("New")
        self.btn_new.clicked.connect(self.on_new)
        self.btn_box0.addWidget(self.btn_new)
        #
        self.btn_open = QPushButton("Open")
        self.btn_open.clicked.connect(self.on_open)
        self.btn_box0.addWidget(self.btn_open)
        #
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["python", "bash", "html"])
        self.lang_combo.currentIndexChanged.connect(self.on_lang_combo)
        self.btn_box0.addWidget(self.lang_combo)
        #
        self.__btn = QPushButton("Exit")
        self.__btn.clicked.connect(self.__btn_action)
        self.btn_box0.addWidget(self.__btn)
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
        if len(sys.argv) > 1:
            filePath = os.path.realpath(sys.argv[1])
            if os.path.exists(filePath):
                self.pageName = filePath
                self.setWindowTitle("{}".format(self.pageName))
        else:
            for el in self.pageNameHistory[::-1]:
                if el.rstrip("\n") == self.pageName:
                    continue
                self.btn_h_menu.addAction(el.rstrip("\n"))
        if self.pageName:
            # populate the menu - opened doc at last position
            self.btn_h_menu.addAction(self.pageName)
            # save into the list once
            if self.pageName+"\n" in self.pageNameHistory:
                self.pageNameHistory.remove(self.pageName+"\n")
            self.pageNameHistory.append(self.pageName+"\n")
        # buttons
        self.btn_box = QHBoxLayout()
        self.__lyt.addLayout(self.btn_box)
        #
        self.btn_ro = QPushButton("Read Only")
        self.btn_ro.clicked.connect(self.on_read_only)
        self.btn_box.addWidget(self.btn_ro)
        #
        self.btn_save = QPushButton("Save")
        self.btn_save.clicked.connect(self.on_save)
        self.btn_box.addWidget(self.btn_save)
        #
        self.btn_save_as = QPushButton("Save as...")
        self.btn_save_as.clicked.connect(self.on_save_as)
        self.btn_box.addWidget(self.btn_save_as)
        #
        self.btn_search = QPushButton("Search")
        self.btn_search.clicked.connect(self.on_search)
        self.btn_box.addWidget(self.btn_search)
        #
        self.btn_comment = QPushButton("Comment")
        self.btn_comment.clicked.connect(self.on_btn_comment)
        self.btn_box.addWidget(self.btn_comment)
        #
        self.btn_uncomment = QPushButton("Uncomment")
        self.btn_uncomment.clicked.connect(self.on_btn_uncomment)
        self.btn_box.addWidget(self.btn_uncomment)
        #
        # ----------------------------------------
        # self.__editor = QsciScintilla()
        self.__editor = MyQsciScintilla()
        #
        try:
            if os.path.exists(self.pageName):
                fd = QFile(self.pageName)
                fd.open(QIODevice.ReadOnly)
                self.__editor.read(fd)
                fd.close()
        except Exception as E:
            MyDialog("Error", str(E), self)
        #
        self.__editor.setLexer(None)            # We install lexer later
        self.__editor.setUtf8(True)             # Set encoding to UTF-8
        self.__editor.setFont(self.__myFont)    # Gets overridden by lexer later on
        # Brace matching
        self.__editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.__editor.setMatchedBraceBackgroundColor(QColor(MATCHEDBRACECOLOR))
        # selected word colour
        self.__editor.setSelectionBackgroundColor(QColor(SELECTIONBACKGROUNDCOLOR))
        #####
        self.__editor.setAutoCompletionThreshold(AUTOCOMPLETITION_CHARS)
        self.__editor.setAutoCompletionCaseSensitivity(True)
        self.__editor.setAutoCompletionReplaceWord(False)
        self.__editor.setAutoCompletionUseSingle(QsciScintilla.AcusNever)
        self.__editor.autoCompleteFromDocument()
        self.__editor.setAutoCompletionSource(QsciScintilla.AcsDocument)
        if USEWORDAUTOCOMLETION:
            self.__editor.setAutoCompletionWordSeparators(["."])
        # End-of-line mode
        # --------------------
        if ENDOFLINE == "unix":
            self.__editor.setEolMode(QsciScintilla.EolUnix)
        elif ENDOFLINE == "windows":
            self.__editor.setEolMode(QsciScintilla.EolWindows)
        #
        self.__editor.setEolVisibility(False)
        # comment string
        self.STRCOMM = "# "
        # Indentation
        # ---------------
        self.__editor.setIndentationsUseTabs(USETAB)
        self.__editor.setTabWidth(TABWIDTH)
        self.__editor.setIndentationGuides(True)
        self.__editor.setTabIndents(True)
        self.__editor.setAutoIndent(True)
        self.__editor.setBackspaceUnindents(True)
        
        # a character has been typed
        self.__editor.SCN_CHARADDED.connect(self.on_k)
        
        # the text has been modified
        self.__editor.modificationChanged.connect(self.on_text_changed)
        
        # Caret
        # ---------
        self.__editor.setCaretForegroundColor(QColor(CARETFORE))
        self.__editor.setCaretLineVisible(True)
        self.__editor.setCaretLineBackgroundColor(QColor(CARETBACK))
        self.__editor.setCaretWidth(CARETWIDTH)
        
        # Margins
        # -----------
        # Margin 0 = Line nr margin
        self.__editor.setMarginType(0, QsciScintilla.NumberMargin)
        self.__editor.setMarginWidth(0, "00000")
        self.__editor.setMarginsForegroundColor(QColor(MARGINFOREGROUND))
        self.__editor.setMarginsFont(self.__myFont)
        #
        # self.__lexer = MyLexer(self.__editor)
        self.__lexer = QsciLexerPython(self.__editor)
        self.__lexer.setDefaultFont(self.__myFont)
        self.__editor.setLexer(self.__lexer)
        #
        
        ##
        # editor background color
        self.__lexer.setPaper(QColor(EDITORBACKCOLOR))
        # comment color
        self.__lexer.setColor(QColor(COMMENTCOLOR), QsciLexerPython.Comment)
        # font
        self.__lexer.setFont(QFont(FONTFAMILY, FONTSIZE))
        
        # ! Add editor to layout !
        # -------------------------
        self.__lyt.addWidget(self.__editor)
        # 
        self.__editor.setContextMenuPolicy(Qt.DefaultContextMenu)
        #
        self.show()
    
    def on_text_changed(self):
        self.isModified = True
        self.setWindowTitle("{} (modified)".format(self.pageName))
    
    # open a file from the history
    def on_h_menu(self, action):
        fileName = action.text()
        self.on_open_f(fileName)
    
    #
    def on_new(self):
        if self.isModified:
            # MyDialog("Info", "Save this document first.", self)
            # return
            ret = retDialogBox("Question", "This document has been modified. \nDo you want to proceed anyway?", self)
            if ret.getValue() == 0:
                return
        self.__editor.setText("")
        self.setWindowTitle("")
        self.isModified = False
        
    #
    def on_open(self):
        if self.isModified:
            # MyDialog("Info", "Save this document first.", self)
            # return
            ret = retDialogBox("Question", "This document has been modified. \nDo you want to proceed anyway?", self)
            if ret.getValue() == 0:
                return
        #
        fileName, _ = QFileDialog.getOpenFileName(self, "Select the file", os.path.expanduser('~'), "Python (*.py);;All Files (*)")
        self.on_open_f(fileName)
        
    # related to on_open
    def on_open_f(self, fileName):
        if fileName == self.pageName:
            MyDialog("Info", "It is the current document.", self)
            return
        # new_tab_to_open = False
        if fileName:
            try:
                fd = QFile(fileName)
                fd.open(QIODevice.ReadOnly)
                self.__editor.setText("")
                self.__editor.read(fd)
                fd.close()
                self.setWindowTitle(fileName)
                self.pageName = fileName
                if not self.pageName+"\n" in self.pageNameHistory:
                    self.btn_h_menu.addAction(self.pageName)
                    self.pageNameHistory.append(self.pageName+"\n")
            except Exception as E:
                MyDialog("Error", str(E), self)
        #
        self.isModified = False
    
    #
    def on_lang_combo(self, idx):
        if idx == 0:
            self.STRCOMM = "# "
            self.__lexer = QsciLexerPython(self.__editor)
            self.__lexer.setDefaultFont(self.__myFont)
            self.__editor.setLexer(self.__lexer)
            # editor background color
            self.__lexer.setPaper(QColor(EDITORBACKCOLOR))
            # comment color
            self.__lexer.setColor(QColor(COMMENTCOLOR), QsciLexerPython.Comment)
            # font
            self.__lexer.setFont(QFont(FONTFAMILY, FONTSIZE))
            # Margin
            self.__editor.setMarginsForegroundColor(QColor(MARGINFOREGROUND))
            self.__editor.setMarginsFont(self.__myFont)
            #
            self.__editor.setAutoCompletionCaseSensitivity(True)
        elif idx == 1:
            self.STRCOMM = "# "
            self.__lexer = QsciLexerBash(self.__editor)
            self.__lexer.setDefaultFont(self.__myFont)
            self.__editor.setLexer(self.__lexer)
            # editor background color
            self.__lexer.setPaper(QColor(EDITORBACKCOLOR))
            # comment color
            self.__lexer.setColor(QColor(COMMENTCOLOR), QsciLexerBash.Comment)
            # font
            self.__lexer.setFont(QFont(FONTFAMILY, FONTSIZE))
            # Margin
            self.__editor.setMarginsForegroundColor(QColor(MARGINFOREGROUND))
            self.__editor.setMarginsFont(self.__myFont)
            #
            self.__editor.setAutoCompletionCaseSensitivity(True)
        elif idx == 2:
            self.STRCOMM = "// "
            self.__lexer = QsciLexerHTML(self.__editor)
            self.__lexer.setDefaultFont(self.__myFont)
            self.__editor.setLexer(self.__lexer)
            # editor background color
            self.__lexer.setPaper(QColor(EDITORBACKCOLOR))
            # # comment color
            # self.__lexer.setColor(QColor(COMMENTCOLOR), QsciLexerHTML.Comment)
            # font
            self.__lexer.setFont(QFont(FONTFAMILY, FONTSIZE))
            # Margin
            self.__editor.setMarginsForegroundColor(QColor(MARGINFOREGROUND))
            self.__editor.setMarginsFont(self.__myFont)
            # 
            self.__editor.setAutoCompletionCaseSensitivity(True)
    
    #
    def on_read_only(self, btn):
        if self.isModified:
            MyDialog("Info", "Save this document first.", self)
            return
        #
        if not self.__editor.isReadOnly():
            self.__editor.setReadOnly(True)
            self.sender().setStyleSheet("QPushButton {color: green;}")
            self.setWindowTitle("{} (read only)".format(self.pageName))
        else:
            self.__editor.setReadOnly(False)
            self.sender().setStyleSheet("")
            self.setWindowTitle("{}".format(self.pageName))
    
    #
    def on_save_as(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "File Name...", self.pageName, "Python (*.py);;All Files (*)")
        if fileName:
            self.pageName = fileName
            self.on_save()
    
    #
    def on_save(self):
        if not self.pageName:
            self.pageName = os.path.join(os.path.expanduser("~"), "document.py")
            self.on_save_as()
            return
        #
        try:
            fd = QFile(self.pageName)
            fd.open(QIODevice.WriteOnly)
            self.__editor.write(fd)
            fd.close()
            #
            self.isModified = False
            self.setWindowTitle("{}".format(self.pageName))
        except Exception as E:
            MyDialog("Error", str(E), self)
    
        
    #
    def on_search(self):
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
                self.__editor.insertAt(self.STRCOMM, line, 0)
        # no selection
        else:
            line, idx = self.__editor.getCursorPosition()
            if self.__editor.text(line) == "":
                return
            # 
            self.__editor.insertAt(self.STRCOMM, line, 0)
    
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
                self.__editor.setCursorPosition(line, 0)
                self.__editor.setSelection(line, 0, line, len(self.STRCOMM))
                self.__editor.removeSelectedText()
        # no selection
        else:
            line, idx = self.__editor.getCursorPosition()
            if self.__editor.text(line) == "":
                return
            self.__editor.setCursorPosition(line, 0)
            self.__editor.setSelection(line, 0, line, len(self.STRCOMM))
            self.__editor.removeSelectedText()
    
    # insert a character if a certain one has been typed
    def on_k(self, id):
        # 40 ( - 39 ' - 34 " - 91 [ - 123 {
        if AUTOCLOSE:
            if id == 40:
                self.__editor.insert(")")
            elif id == 39:
                self.__editor.insert("'")
            elif id == 34:
                self.__editor.insert('"')
            elif id == 91:
                self.__editor.insert(']')
            elif id == 123:
                self.__editor.insert('}')
        #
        # the document has been modified
        if not self.isModified:
            self.isModified = True
            self.setWindowTitle("{} (modified)".format(self.pageName))
    
    def wheelEvent(self, e):
        if e.modifiers() & Qt.CTRL:
            if e.angleDelta().y() < 0:
                self.__editor.zoomOut()
            else:
                self.__editor.zoomIn()
    
    def __btn_action(self):
        if self.isModified:
            ret = retDialogBox("Question", "This document has been modified. \nDo you want to proceed anyway?", self)
            if ret.getValue() == 0:
                return
        self.close()
    
    def closeEvent(self, event):
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
        self.setWindowIcon(QIcon("icons/program.svg"))
        self.setWindowTitle("Search...")
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(DIALOGWIDTH, 300)
        #
        vbox = QBoxLayout(QBoxLayout.TopToBottom)
        vbox.setContentsMargins(5,5,5,5)
        self.setLayout(vbox)
        #
        self.line_edit = QLineEdit()
        if ret_text:
            self.line_edit.setText(ret_text)
        vbox.addWidget(self.line_edit)
        ### button box
        hbox = QBoxLayout(QBoxLayout.LeftToRight)
        vbox.addLayout(hbox)
        #
        button4 = QPushButton("Previous")
        button4.clicked.connect(lambda:self.on_find(0))
        hbox.addWidget(button4)
        #
        button2 = QPushButton("Next")
        button2.clicked.connect(lambda:self.on_find(1))
        hbox.addWidget(button2)
        #
        button3 = QPushButton("Close")
        button3.clicked.connect(self.close)
        hbox.addWidget(button3)
        #
        self.first_found = False
        self.isForward = True
        #
        self.Value = 0
        #
        self.exec_()
        
    def on_find(self, ftype):
        line_edit_text = self.line_edit.text()
        if ftype:
            if not self.first_found or not self.isForward:
                self.isForward = True
                ret = self.editor.findFirst(line_edit_text, False, False, False, False, True)#, -1, -1, True, True)
                self.first_found = ret
            else:
                self.editor.findNext()
        else:
            if not self.first_found or self.isForward:
                self.isForward = False
                ret = self.editor.findFirst(line_edit_text, False, False, False, False, False)
                self.first_found = ret
            else:
                self.editor.findNext()
        
    
    # def on_accept(self):
        # if self.win_list.currentItem():
            # data_get = self.win_list.currentItem().text()
            # self.Value = data_get
        # self.close()
    
    def getValue(self):
        return self.Value


# dialog - return of the choise yes or no
class retDialogBox(QMessageBox):
    def __init__(self, *args):
        super(retDialogBox, self).__init__(args[-1])
        self.setWindowIcon(QIcon("icons/progam.png"))
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
    myGUI = CustomMainWindow()
    sys.exit(app.exec_())
    
########################
