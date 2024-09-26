import os
from PyQt5.QtWidgets import QMainWindow,QWidget, QVBoxLayout, QHBoxLayout,QMessageBox, QProgressBar,QLabel, QPushButton,QAction, QShortcut,QFileDialog, QMenu,QSizePolicy
from PyQt5.QtGui import QKeySequence, QPixmap,QKeyEvent
from PyQt5.QtCore import Qt

from package.fileHandler import fileHandler
from package.photoGalery import photoGalery
from package.photoHandler import photoHandler
from package.photoboothMode import photoboothMode
from package.printerHandler import printerHandler
from package.sideControl import sideControl

class mainWindow(QWidget):
    defaultPath = r"assets/defaultImg.webp"
    brokenPath = r"assets/brokenImg.webp"
    def __init__(self, app):
        self.app = app
        super().__init__()

        self.initVariables()
        self.initWindow()
        self.photoBooth = None

        #self.showMaximized()

        self.photoHandler.OnNewThumbNail.connect(self.galery.addThumbnail)
        self.updateMainLab()
        self.galery.loadAllThumbnails()
        self.showMaximized()

        
        
        #self.startPhotoBooth()

    def initVariables(self):
        self.fileHandler = fileHandler()
        self.fileHandler.ejectError.connect(self.showWarning)
        self.fileHandler.transferDone.connect(self.showMsg)

        self.printerHandler = printerHandler()

        self.currentImage = self.defaultPath

        self.photoHandler = photoHandler(self.fileHandler)
        

        self.pix = QPixmap()

    def initWindow(self):
        #baue die Struktur auf!
        self.lay = QVBoxLayout()

        #Hauptfenster:
        self.mainLab = QLabel("Test")
        self.mainLab.setMinimumSize(800,800)
        self.mainLab.setScaledContents(True)


        #Setenfenster
        self.sideCont = sideControl(self,self.printerHandler)

        #Galiere
        self.galery = photoGalery(self,self.photoHandler)


        topLay = QHBoxLayout()
        topLay.addWidget(self.mainLab)
        topLay.addStretch(1)
        topLay.addWidget(self.sideCont)


        self.lay.addLayout(topLay,stretch=3)
        self.lay.addWidget(self.galery,stretch=1)

        self.setLayout(self.lay)


    def resizeEvent(self, event):
        """Override the resize event to update the QLabel's pixmap size dynamically."""
        self.update_pixmap()
        super().resizeEvent(event)

    def update_pixmap(self):

        # Get the current size of the window (or parent container)
        
        container_height = self.height()

        #Label bekommt 70%
        labHeight = int(container_height*0.65)
        pixmap_width = self.pix.width()
        pixmap_height = self.pix.height()
        aspect_ratio = pixmap_width / pixmap_height
       
        new_height = labHeight
        new_width = int(new_height * aspect_ratio)


        # Scale the pixmap to the new dimensions, keeping the aspect ratio
        scaled_pixmap = self.pix.scaled(
            new_width, new_height, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )

        # Set the scaled pixmap to the QLabel
        self.mainLab.setPixmap(scaled_pixmap)

        # Resize the QLabel to fit the scaled pixmap
        self.mainLab.setFixedSize(scaled_pixmap.size())
    def updateMainLab(self):
        #lade das Bild
        self.pix = QPixmap(self.currentImage)
        if self.pix.isNull():
            self.pix = QPixmap(self.brokenPath)

        self.mainLab.setPixmap(self.pix)
        self.update_pixmap()


    def closeEvent(self, event):
        if self.photoBooth != None:
            self.photoBooth.close()
        self.fileHandler.killThread()


    def showMsg(self, lenFiles):
        msg = QMessageBox()
        msg.setWindowTitle("Erfolg!")
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"Erfolgreich {lenFiles} Daten kopiert. Die SD Karte wurde ebenfalls ausgeworfen. Bitte Drücke den Schalter, um die Kamera wieder zu aktivieren!")
        msg.exec_()

    def showWarning(self, lenFiles, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Problem beim Auswerfen!")
        msg.setText(f"Erfolgreich {lenFiles} Daten kopiert. Aber die SD Karte wurde nicht ausgeworfen! Bitte wirf die manuell aus und dann drücke den Schalter! Oder drück einfach nur den Schalter. Ich bin nur ein Schild und kein Cop!\n\nFalls es dich interessiert, hier ist die Fehlermeldung:\n{message}")
        msg.exec_()


    def startPhotoBooth(self):
        self.photoBooth = photoboothMode(self,self.photoHandler)

    def photoBoothStopped(self):
        self.photoBooth = None

    def newImageClicked(self,filename):
        self.currentImage = os.path.join(self.fileHandler.aimFolder,filename)
        print(self.currentImage)
        self.updateMainLab()

    def newImageTaken(self,fileName):
        self.photoHandler.lookForImages()


    def printImage(self, imageToPrint):
        self.printerHandler.printImage(imageToPrint)


    