import sys
import cx_Freeze

executables = [cx_Freeze.Executable("Main.py",base="Win32GUI",shortcutName="Text_Editor",shortcutDir="DesktopFolder",icon="text_editor.ico",targetName="Text_editor.exe",)]

includefiles = ["setting.json","Welcome.txt", "icons","Themes","textedit.qrc","text_editor.png"]


cx_Freeze.setup(
    name="Text Editor",
    version ="1.0",
    author="Nitin Upadhyay",
    options={"build_exe":{"packages":[], 'include_files':includefiles}},
    description = "Notepad by Nitin Upadhyay",
    executables = executables
    )
