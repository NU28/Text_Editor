# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Text_editor.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

class Ui_TextEditor(object):
    def setupUi(self, MainWindow):
        self.setToolButtonStyle(Qt.ToolButtonFollowStyle)
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.textEdit.setFocus()
        self.setWindowIcon(QIcon("text_editor.png"))
        self.newAction = QAction(QIcon("icons/new.png"), "&New", self)
        self.openAction = QAction(QIcon("icons/open.png"), "&Open", self)
        self.saveAction = QAction(QIcon("icons/save.png"), "&Save", self)
        self.saveAsAction = QAction(QIcon("icons/save_as.png"), "&Save", self)
        self.printAction = QAction(QIcon("icons/print.png"), "&Print", self)
        self.printPreview = QAction(QIcon("icons/printpreview.png"), "&Print Preview", self)
        self.pdfAction = QAction(QIcon("icons/exportpdf.png"), "Export PDF", self)
        self.exitAction = QAction(QIcon("icons/exit.png"), "&Exit", self)
        self.undoAction = QAction(QIcon("icons/undo.png"), "&Undo", self)
        self.redoAction = QAction(QIcon("icons/redo.png"), "&Redo", self)
        self.cutAction = QAction(QIcon("icons/cut.png"), "&Cut", self)
        self.copyAction = QAction(QIcon("icons/copy.png"), "&Copy", self)
        self.pasteAction = QAction(QIcon("icons/paste.png"), "&Paste", self)
        self.fontAction = QAction(QIcon("icons/font.png"), "&Font", self)
        self.boldAction = QAction(QIcon("icons/bold.png"), "&Bold", self)
        self.italicAction = QAction(QIcon("icons/italic.png"), "&Italic", self)
        self.underlineAction = QAction(QIcon("icons/underline.png"), "&Underline", self)
        self.strikeAction = QAction(QIcon("icons/strikeout.png"), "&Strike", self)
        self.colorAction = QAction(QIcon("icons/color.png"), "&Text Color", self)
        self.superScriptAction = QAction(QIcon("icons/superscript.png"), "&Super Script", self)
        self.subscriptAction = QAction(QIcon("icons/subscript.png"), "&Sub Script", self)
        self.alignLeft = QAction(QIcon("icons/left.png"), "Align left", self)
        self.alignCenter = QAction(QIcon("icons/center.png"), "Align center", self)
        self.alignRight = QAction(QIcon("icons/right.png"), "Align right", self)
        self.alignJustify = QAction(QIcon("icons/justify.png"), "Align justify", self)
        self.highlighterAction = QAction(QIcon("icons/highlighter.png"), "Text Highlighter", self)
        self.datetime = QAction(QIcon("icons/datetime.png"), "Date and Time", self)
        self.aboutAction = QAction(QIcon("icons/about.png"), "About", self)
        self.findAction =QAction(QIcon("icons/find.png"), "Find and Replace...", self)


        menubar = self.menuBar()

        # FileMenu
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveAsAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.printAction)
        fileMenu.addAction(self.printPreview)
        fileMenu.addSeparator()
        fileMenu.addAction(self.pdfAction)
        fileMenu.addAction(self.exitAction)

        # EditMenu
        editMenu = menubar.addMenu("&Edit")
        editMenu.addAction(self.undoAction)
        editMenu.addAction(self.redoAction)
        editMenu.addSeparator()
        editMenu.addAction(self.cutAction)
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addSeparator()
        editMenu.addAction(self.findAction)
        editMenu.addAction(self.datetime)

        # FormatMenu
        formatMenu = menubar.addMenu("&Format")
        formatMenu.addAction(self.fontAction)
        formatMenu.addAction(self.colorAction)

        # StyleMenu
        styleMenu = menubar.addMenu("&Style")
        styleMenu.addAction(self.boldAction)
        styleMenu.addAction(self.italicAction)
        styleMenu.addAction(self.underlineAction)
        styleMenu.addSeparator()
        styleMenu.addAction(self.alignLeft)
        styleMenu.addAction(self.alignRight)
        styleMenu.addAction(self.alignCenter)
        styleMenu.addAction(self.alignJustify)
        styleMenu.addSeparator()
        styleMenu.addAction(self.highlighterAction)



        # HelpMenu
        helpMenu = menubar.addMenu("&Help")
        helpMenu.addAction(self.aboutAction)

        # -------------------------------------------------------------------xx------------------------------------------------------------------------------------
        # -------------------------------------------------------------------xx------------------------------------------------------------------------------------

        # --------------------------------------------------------------------ToolBar------------------------------------------------------------------------------

        # ToolBar

        self.file_toolbar = self.addToolBar("File")
        self.file_toolbar.addAction(self.newAction)
        self.file_toolbar.addAction(self.openAction)
        self.file_toolbar.addAction(self.saveAction)
        self.file_toolbar.addAction(self.saveAsAction)
        self.file_toolbar.addAction(self.printAction)
        self.file_toolbar.addAction(self.exitAction)

        self.toolbar = self.addToolBar("Edit")
        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)
        self.toolbar.addAction(self.cutAction)
        self.toolbar.addAction(self.copyAction)
        self.toolbar.addAction(self.pasteAction)

        self.toolbar = self.addToolBar("Format")
        self.toolbar.addAction(self.fontAction)
        self.toolbar.addAction(self.highlighterAction)

        self.toolbar.addAction(self.boldAction)
        self.toolbar.addAction(self.italicAction)
        self.toolbar.addAction(self.underlineAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.strikeAction)
        self.toolbar.addAction(self.superScriptAction)
        self.toolbar.addAction(self.subscriptAction)
        self.toolbar.addSeparator()

        self.toolbar.addAction(self.datetime)
        self.toolbar.addAction(self.alignLeft)
        self.toolbar.addAction(self.alignCenter)
        self.toolbar.addAction(self.alignRight)
        self.toolbar.addAction(self.alignJustify)
        self.toolbar.addSeparator()

        # -------------------------------------------------StatusBar------------------------------
        self.status = self.statusBar()
        self.textEdit.cursorPositionChanged.connect(self.CursorPosition)

    def CursorPosition(self):
        line = self.textEdit.textCursor().blockNumber()
        col = self.textEdit.textCursor().columnNumber()
        linecol = ("Line: " + str(line) + " | " + "Column: " + str(col))
        self.status.showMessage(linecol)