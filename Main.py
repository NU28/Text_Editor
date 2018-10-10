import sys
from TextEditorwindow import EditorWindow
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
textEditor = EditorWindow()
sys.exit(app.exec())

