import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication,QWidget,QStackedWidget

class start_screen(QDialog):
    def __init__(self):
        super(start_screen,self).__init__()
        loadUi('../GUI_main.ui',self)
        self.selectl.clicked.connect(self.gotoselect)
        self.addl.clicked.connect(self.gotoadd)

    def gotoselect(self):
        select=select_screen()
        widget.addWidget(select)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoadd(self):
        add_l=add_screen()
        widget.addWidget(add_l)
        widget.setCurrentIndex(widget.currentIndex()+2)

class select_screen(QDialog):
    def __init__(self):
        super(select_screen,self).__init__()
        loadUi('../GUI.ui',self)

class add_screen(QDialog):
    def __init__(self):
        super(add_screen,self).__init__()
        loadUi('../GUI_add.ui',self)

app=QApplication(sys.argv)
start=start_screen()
widget=QStackedWidget()
widget.addWidget(start)
widget.setFixedHeight(700)
widget.setFixedWidth(800)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print('exiting')