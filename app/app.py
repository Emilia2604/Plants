import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication,QWidget,QStackedWidget

from db_conn import add_set, plant_list, find_spectrum

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

        self.plantsbox.addItems(plant_list())

        self.b_germination.clicked.connect(self.show_germ)
        self.b_vegetation.clicked.connect(self.show_veg)
        self.b_flowering.clicked.connect(self.show_flow)
        self.b_fruits.clicked.connect(self.show_fru)

    def set_spectrum(self,dict_led):
        self.spin_uv.setValue(dict_led['uv'])
        self.spin_royal.setValue(dict_led['royal blue'])
        self.spin_white.setValue(dict_led['white'])
        self.spin_red.setValue(dict_led['red'])
        self.spin_photo.setValue(dict_led['photo red'])

    def show_germ(self):
        self.set_spectrum(find_spectrum('germination',self.plants_box.currentText()))

    def show_veg(self):
        self.set_spectrum(find_spectrum('vegetation',self.plants_box.currentText()))

    def show_flow(self):
        self.set_spectrum(find_spectrum('flowering',self.plants_box.currentText()))
    
    def show_fru(self):
        self.set_spectrum(find_spectrum('fruits',self.plants_box.currentText()))

class add_screen(QDialog):
    def __init__(self):
        super(add_screen,self).__init__()
        loadUi('../GUI_add.ui',self)
        self.add_b.clicked.connect(self.add_set)
        self.spectrum=[]
        self.leds=['uv','royal blue','white','red','photo red']
        self.list_stage=['germination','vegetation','flowering','fruits']
        self.stage_box.addItems(self.list_stage)

    def up_spectrum(self):
        self.spectrum[0]=self.uv_spin.value()
        self.spectrum[1]=self.royal_spin.value()
        self.spectrum[2]=self.white_spin.value()
        self.spectrum[3]=self.red_spin.value()
        self.spectrum[4]=self.photo_spin.value()

    def add_set(self):
        self.up_spectrum()
        self.list_set=[self.stage_box.currentText(),'uv','0']
        self.list_set[3]=self.name_plant.text()
        for x in range(len(self.spectrum)):
            self.list_set[1]=self.leds[x]
            self.list_set[2]=self.spectrum[x]
            add_set(list_set)


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