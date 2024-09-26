from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap,QColor,QIcon
from PyQt5.QtCore import QSize
from package.printerHandler import printerHandler

class sideControl(QWidget):
    printerImage= r"assets/printer.webp"
    cameraImage= r"assets/camera.webp"
    def __init__(self,superior, prinHan:printerHandler):
        super().__init__()
        self.superior = superior
        self.printerHandler = prinHan
                
        self.lay = QVBoxLayout()


        desc = QLabel("Printer:")
        self.printerLab = QLabel()
        self.printerStatus = QLabel()
        pLay = QHBoxLayout()
        pLay.addWidget(desc)
        pLay.addWidget(self.printerLab)
        pLay.addWidget(self.printerStatus)

        #self.lay.addLayout(pLay)
        self.setLayout(self.lay)

        btnS = 300
        btnB = 20
        self.printBtn = QPushButton("")
        self.printBtn.setIcon(QIcon(self.printerImage))
        self.printBtn.setFixedSize(btnS,btnS)
        self.printBtn.setIconSize(QSize(btnS-btnB,btnS-btnB))
        self.printBtn.clicked.connect(self.printImage)
        self.lay.addWidget(self.printBtn)
        self.good = QPixmap(25,25)
        self.good.fill(QColor(0,255,0))
        self.bad = QPixmap(25,25)
        self.bad.fill(QColor(255,0,0))



        self.photoBoothBtn = QPushButton("")
        self.photoBoothBtn.clicked.connect(self.startPhotoBooth)

        self.photoBoothBtn.setIcon(QIcon(self.cameraImage))
        self.photoBoothBtn.setFixedSize(btnS,btnS)
        self.photoBoothBtn.setIconSize(QSize(btnS-btnB,btnS-btnB))
        self.lay.addWidget(self.photoBoothBtn)
        self.lay.addStretch(1)
        #self.updatePrinterStatus()


    def printImage(self):
        self.printerHandler.printImage(self.superior.currentImage)
    def updatePrinterStatus(self):
        self.printerLab.setText(self.printerHandler.printer_name)
        if(self.printerHandler.is_printer_available()):
            self.printerStatus.setPixmap(self.good)
            self.printBtn.setEnabled(True)
        else:
            self.printerStatus.setPixmap(self.bad)
            self.printBtn.setEnabled(False)



    def startPhotoBooth(self):
        self.superior.startPhotoBooth()