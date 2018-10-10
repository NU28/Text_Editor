import PyQt5
import txt_editor
from txt_editor import Ui_TextEditor
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtCore import *
import about
from about import *
import textedit_rc3
import json
if sys.platform.startswith('darwin'):
    rsrcPath = ":/images/mac"
else:
    rsrcPath = ":/images/win"

var = 0
f = ""
choiceStr = ""
cs = False
wwo = False

tt = True
tf = True
ts = True


class Find(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.initUI()

    def initUI(self):

        self.lb1 = QLabel("Search for: ", self)
        self.lb1.setStyleSheet("font-size: 15px; ")
        self.lb1.move(10, 10)

        self.te = QTextEdit(self)
        self.te.move(10, 40)
        self.te.resize(250, 25)

        self.src = QPushButton("Find", self)
        self.src.move(270, 40)

        self.lb2 = QLabel("Replace all by: ", self)
        self.lb2.setStyleSheet("font-size: 15px; ")
        self.lb2.move(10, 80)

        self.rp = QTextEdit(self)
        self.rp.move(10, 110)
        self.rp.resize(250, 25)

        self.rpb = QPushButton("Replace", self)
        self.rpb.move(270, 110)

        self.opt1 = QCheckBox("Case sensitive", self)
        self.opt1.move(10, 160)
        self.opt1.stateChanged.connect(self.CS)

        self.opt2 = QCheckBox("Whole words only", self)
        self.opt2.move(10, 190)
        self.opt2.stateChanged.connect(self.WWO)

        self.close = QPushButton("Close", self)
        self.close.move(270, 220)
        self.close.clicked.connect(self.Close)

        self.setGeometry(300, 300, 360, 250)

    def CS(self, state):
        global cs

        if state == Qt.Checked:
            cs = True
        else:
            cs = False

    def WWO(self, state):
        global wwo

        if state == Qt.Checked:
            wwo = True
        else:
            wwo = False

    def Close(self):
        self.hide()

class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        quotationColor = "rgb(195,232,141)"
        classfunctionColor = "rgb(255,203,107)"
        keywordColor = "rgb(183,146,234)"
        functionColor = "rgb(137,215,217)"
        commentColor = "rgb(247,118,105)"

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(183, 146, 234))
        keywordFormat.setFontWeight(QFont.Bold)
        keywordPatterns = ["\\bFalse\\b", "\\bNone\\b", "\\bTrue\\b", "\\band\\b", "\\bas\\b",
                           "\\bassert\\b", "\\bbreak\\b", "\\bcontinue\\b",
                           "\\bdel\\b", "\\belif\\b", "\\belse\\b", "\\bexcept\\b", "\\bfinally\\b",
                           "\\bfor\\b", "\\bfrom\\b", "\\bglobal\\b", "\\bif\\b", "\\bimport\\b",
                           "\\bin\\b", "\\bis\\b", "\\blambda\\b", "\\bnonlocal\\b", "\\bnot\\b",
                           "\\bor\\b", "\\bpass\\b", "\\braise\\b", "\\breturn\\b", "\\btry\\b",
                           "\\bwhile\\b", "\\bwith\\b", "\\byield\\b", "\\print\\b"]
        self.highlightingRules = [(QRegExp(pattern), keywordFormat)
                                  for pattern in keywordPatterns]

        classRegExp = "\\bclass\s[A-Za-z_]+\\b"
        classFormat = QTextCharFormat()
        classFormat.setForeground(QColor(255, 203, 107))
        classFormat.setFontWeight(QFont.Bold)
        self.highlightingRules.append((QRegExp(classRegExp), classFormat))

        defRegExp = "\\bdef\s[A-Za-z_]+\\b"
        defFormat = QTextCharFormat()
        defFormat.setForeground(QColor(255, 203, 107))
        defFormat.setFontWeight(QFont.Bold)
        self.highlightingRules.append((QRegExp(defRegExp), defFormat))

        singleLineCommentExp = "#[^\n]*"
        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setForeground(QColor(247, 118, 105))
        self.highlightingRules.append((QRegExp(singleLineCommentExp), singleLineCommentFormat))

        quotationExp = "\".*\""

        quotationFormat = QTextCharFormat()
        # quotationFormat.setFontItalic(True)
        quotationFormat.setForeground(QColor(195, 232, 141))
        self.highlightingRules.append((QRegExp(quotationExp), quotationFormat))

        functionExp = "\\[A-Za-z0-9_]+(?=\\()"
        functionFormat = QTextCharFormat()
        functionFormat.setForeground(QColor(137, 215, 217))
        functionFormat.setFontWeight(QFont.Bold)
        self.highlightingRules.append((QRegExp(functionExp), functionFormat))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

class EditorWindow(QMainWindow, Ui_TextEditor):
    def __init__(self, fileName=None, parent=None):
        super(EditorWindow,self).__init__(parent)
        self.setupUi(self)
        self.setMinimumSize(600,400)
        self.showMaximized()
        self.setWindowIcon(QIcon("text_editor.png"))

        setting_ = open("setting.json", "r")
        json_file = json.loads(setting_.read())
        font_name = json_file["fonts"]["font-name"]
        font_size = int(json_file["fonts"]["font-size"])
        # StyleSheet = json_file["themes"]["logo-color"]
        theme_name = str(json_file["themes"]["style"])
        style_name = "Themes/" + theme_name + ".ini"

        style_file = open(style_name, "r")
        style_theme = str(style_file.read())
        style_file.close()
        theme_ = str(json_file["themes"]["theme"])
        setting_.close()

        self.setStyleSheet(style_theme)
        QApplication.setStyle(QStyleFactory.create(theme_))
        self.textEdit.setFont(QFont(font_name, font_size))
        self.highlighter = Highlighter(self.textEdit.document())



        if fileName is None:
            fileName = 'Welcome.txt'

        if not self.load(fileName):
            self.new_file()

        self.newAction.setShortcut("Ctrl+N")
        self.newAction.setStatusTip("New File")
        self.newAction.triggered.connect(self.new_file)

        self.openAction.setShortcut("Ctrl+O")
        self.openAction.setStatusTip("Open File")
        self.openAction.triggered.connect(self.open_file)

        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.setStatusTip("Save File")
        self.saveAction.triggered.connect(self.save_file)

        self.saveAsAction.setShortcut("Ctrl+Alt+s")
        self.saveAsAction.setStatusTip("Save As")
        self.saveAsAction.triggered.connect(self.saveAs_file)

        self.printAction.setShortcut("Ctrl+P")
        self.printAction.setStatusTip("Print")
        self.printAction.triggered.connect(self.print_file)

        self.printPreview.setShortcut("Ctrl+Alt+P")
        self.printPreview.setStatusTip("Print Preview")
        self.printPreview.triggered.connect(self.print_Preview)

        # Edit
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.setStatusTip("Undo")
        self.undoAction.triggered.connect(self.textEdit.undo)

        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.setStatusTip("Redo")
        self.redoAction.triggered.connect(self.textEdit.redo)

        self.cutAction.setShortcut("Ctrl+X")
        self.cutAction.setStatusTip("Cut")
        self.cutAction.triggered.connect(self.textEdit.cut)

        self.copyAction.setShortcut("Ctrl+C")
        self.copyAction.setStatusTip("Copy")
        self.copyAction.triggered.connect(self.textEdit.copy)

        self.pasteAction.setShortcut("Ctrl+V")
        self.pasteAction.setStatusTip("Paste")
        self.pasteAction.triggered.connect(self.textEdit.paste)

        self.exitAction.setShortcut("Ctrl+E")
        self.exitAction.setStatusTip("Exit")
        self.exitAction.triggered.connect(self.exit_app)

        # BISSU action
        self.boldAction.setShortcut("Ctrl+B")
        self.boldAction.setStatusTip("Bold")
        self.boldAction.triggered.connect(self._bold)

        self.italicAction.setShortcut("Ctrl+I")
        self.italicAction.setStatusTip("Italic")
        self.italicAction.triggered.connect(self._italic)

        self.underlineAction.setShortcut("Ctrl+U")
        self.underlineAction.setStatusTip("Underline")
        self.underlineAction.triggered.connect(self._underline)

        self.strikeAction.setShortcut("Ctrl+Shift+S")
        self.strikeAction.setStatusTip("Strike Through.png")
        self.strikeAction.triggered.connect(self._strike)

        self.superScriptAction.setShortcut("Ctrl+Shift+U")
        self.superScriptAction.setStatusTip("Super Script")
        self.superScriptAction.triggered.connect(self._superScript)

        self.subscriptAction.setShortcut("Ctrl+Shift+L")
        self.subscriptAction.setStatusTip("Sub Script")
        self.subscriptAction.triggered.connect(self._subscript)

        self.alignLeft.triggered.connect(self._alignLeft)
        self.alignCenter.triggered.connect(self._alignCenter)
        self.alignRight.triggered.connect(self._alignRight)
        self.alignJustify.triggered.connect(self._alignJustify)

        # Format action
        self.fontAction.setShortcut("F3")
        self.fontAction.setStatusTip("Font")
        self.fontAction.triggered.connect(self.font_dialog)

        self.colorAction.setShortcut("Ctrl+Shift+O")
        self.colorAction.setStatusTip("Text Color")
        self.colorAction.triggered.connect(self.color_dialog)

        self.highlighterAction.setShortcut("Ctrl+H")
        self.highlighterAction.setStatusTip("Text Highlighter")
        self.highlighterAction.triggered.connect(self.texthighlighter)

        self.datetime.setShortcut("Ctrl+D")
        self.datetime.setStatusTip("Date and Time")
        self.datetime.triggered.connect(self.dateTime)

        self.aboutAction.setShortcut("Ctrl+M")
        self.aboutAction.setStatusTip("About Us")
        self.aboutAction.triggered.connect(self.about_dialog)

        self.pdfAction.setStatusTip("Export PDF")
        self.pdfAction.triggered.connect(self.exportPdf)

        self.findAction.setStatusTip("Find and words in your document")
        self.findAction.setShortcut("Ctrl+F")
        self.findAction.triggered.connect(self.Find)

        self.show()

    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def Find(self):
        global f

        find = Find(self)
        find.show()

        def handleFind():

            f = find.te.toPlainText()

            if cs == True and wwo == False:
                flag = QTextDocument.FindBackward and QTextDocument.FindCaseSensitively

            elif cs == False and wwo == False:
                flag = QTextDocument.FindBackward

            elif cs == False and wwo == True:
                flag = QTextDocument.FindBackward and QTextDocument.FindWholeWords

            elif cs == True and wwo == True:
                flag = QTextDocument.FindBackward and QTextDocument.FindCaseSensitively and QTextDocument.FindWholeWords

            self.textEdit.find(f, flag)

        def handleReplace():
            f = find.te.toPlainText()
            r = find.rp.toPlainText()

            text = self.textEdit.toPlainText()

            newText = text.replace(f, r)

            self.textEdit.clear()
            self.textEdit.append(newText)

        find.src.clicked.connect(handleFind)
        find.rpb.clicked.connect(handleReplace)


    def exportPdf(self):
        fn, _ = QFileDialog.getSaveFileName(self, "Export PDF", None, "PDF files (.pdf) ;; All Files")
        if fn != "":
            if QFileInfo(fn).suffix() == "" :fn += '.pdf'
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(fn)
            self.textEdit.document().print_(printer)

    def print_Preview(self):
        printer = QPrinter(QPrinter.HighResolution)
        previewDialog = QPrintPreviewDialog(printer, self)
        previewDialog.paintRequested.connect(self.print_Prevew)
        previewDialog.exec_()
    def print_Prevew(self, printer):
        self.textEdit.print_(printer)

    def about_dialog(self):
        tab = TabDialog()
        tab.exec_()

    def new_file(self):
        if self.maybeSave():
            self.textEdit.clear()
            self.setCurrentFileName()

    def open_file(self):
        fileName = QFileDialog.getOpenFileName(self, "Open file", ".", "(*.*)")
        if fileName:
            self.load(fileName)

    def saveAs_file(self):
        fn = QFileDialog.getSaveFileName(self, "Save file")

        if not fn:
            return False

        lfn = fn.lower()
        # if not lfn.endswith(('.txt', '.py', '.html')):
        # # The default.
        #     fn += '.txt'
        self.setCurrentFileName(fn)
        return self.save_file()

    def save_file(self):
        if not self.fileName:
            return self.saveAs_file()
        if self.fileName:
            file = open(self.fileName, "w")
            success = data = self.textEdit.toPlainText()
            file.write(data)
            file.close()
            if success:
                self.textEdit.document().setModified(False)
            return success

    def print_file(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)

        if dialog.exec_() == QPrintDialog.Accepted:
            self.textEdit.print_(printer)

    def exit_app(self):
        choice = QMessageBox.question(self, "Quit", "You Are Really Wanna Quit...", QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def _bold(self):
        if self.textEdit.fontWeight() == QFont.Bold:

            self.textEdit.setFontWeight(QFont.Normal)

        else:

            self.textEdit.setFontWeight(QFont.Bold)

    def _italic(self):

        state = self.textEdit.fontItalic()
        self.textEdit.setFontItalic(not state)

    def _underline(self):
        state = self.textEdit.fontUnderline()
        self.textEdit.setFontUnderline(not state)

    def _strike(self):
        fmt = self.textEdit.currentCharFormat()
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())
        self.textEdit.setCurrentCharFormat(fmt)

    def _superScript(self):
        fmt = self.textEdit.currentCharFormat()
        align = fmt.verticalAlignment()
        if align == QTextCharFormat.AlignNormal:
            fmt.setVerticalAlignment(QTextCharFormat.AlignSuperScript)
        else:
            fmt.setVerticalAlignment(QTextCharFormat.AlignNormal)
        self.textEdit.setCurrentCharFormat(fmt)

    def _subscript(self):
        fmt = self.textEdit.currentCharFormat()
        align = fmt.verticalAlignment()
        if align == QTextCharFormat.AlignNormal:
            fmt.setVerticalAlignment(QTextCharFormat.AlignSubScript)
        else:
            fmt.setVerticalAlignment(QTextCharFormat.AlignNormal)
        self.textEdit.setCurrentCharFormat(fmt)

    def _alignLeft(self):
        self.textEdit.setAlignment(Qt.AlignLeft)

    def _alignRight(self):
        self.textEdit.setAlignment(Qt.AlignRight)

    def _alignCenter(self):
        self.textEdit.setAlignment(Qt.AlignCenter)

    def _alignJustify(self):
        self.textEdit.setAlignment(Qt.AlignJustify)

    def texthighlighter(self):
        c = QColorDialog.getColor()
        self.textEdit.setTextBackgroundColor(c)

    def dateTime(self):
        datetime = QDateTime.currentDateTime()
        self.textEdit.setText(datetime.toString(Qt.DefaultLocaleLongDate))

    def font_dialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.textEdit.setFont(font)

    def color_dialog(self):
        color = QColorDialog.getColor()
        self.textEdit.setTextColor(color)

    def CursorPosition(self):
        line = self.textEdit.textCursor().blockNumber()
        col = self.textEdit.textCursor().columnNumber()
        linecol = ("Line: " + str(line) + " | " + "Column: " + str(col))
        self.status.showMessage(linecol)

    def load(self, f):
        if not QFile.exists(f):
            return False

        fh = QFile(f)
        if not fh.open(QFile.ReadOnly):
            return False

        data = fh.readAll()
        codec = QTextCodec.codecForHtml(data)
        unistr = codec.toUnicode(data)

        if Qt.mightBeRichText(unistr):
            self.textEdit.setHtml(unistr)
        else:
            self.textEdit.setPlainText(unistr)

        self.setCurrentFileName(f)
        return True

    def maybeSave(self):
        if not self.textEdit.document().isModified():
            return True
        if self.fileName.startswith(":/"):
            return True
        ret = QMessageBox.warning(self, "Application","The document has been modified.\n"
                "Do you want to save your changes?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

        if ret == QMessageBox.Save:
            return self.save_file()

        if ret == QMessageBox.Cancel:
            return False

        return True

    def setCurrentFileName(self, fileName=''):
        self.fileName = fileName
        self.textEdit.document()
        if not fileName:
            shownName = 'untitled.txt'
        else:
            # shownName = QFileInfo(fileName).fileName()
            shownName = self.fileName
        self.setWindowTitle(self.tr("%s[*] - %s" % (shownName, "Text Editor")))
        self.setWindowModified(False)

