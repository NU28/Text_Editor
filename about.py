import sys
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import json

class TabDialog(QDialog):
    def __init__(self):
        super(TabDialog,self).__init__()
        self.setWindowTitle("About")
        # self.setWindowIcon(QIcon("_setting.png"))
        intro = QLabel("\tDeveloped by :- \n\n\tNitin Upadhyay\n\tShobhit Singh\n\n")
        roll = QLabel("\tCSE 3th Year from \n\tMAHARAJA SURAJMAL INSTITUTE OF TECHNOLOGY\n")
        pyth = QLabel("\tUsing Python plugin PyQt5")
        thank = QLabel("\n\tThank You!!")
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(intro)
        mainLayout.addWidget(roll)
        mainLayout.addWidget(pyth)
        mainLayout.addWidget(thank)
        
        self.setLayout(mainLayout)
        # setting_ = open("setting.json","r")
        # json_file = json.loads(setting_.read())
        # theme_name = json_file["themes"]["style"]
        # setting_.close()
        #
        # style_name = "Themes/" + theme_name +".ini"
        # style_file = open(style_name, "r")
        # style_theme = str(style_file.read())
        # style_file.close()
        # self.setStyleSheet(style_theme)
        self.show()
