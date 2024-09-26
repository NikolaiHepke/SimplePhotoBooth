import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout,QMessageBox, QProgressBar,QLabel, QPushButton,QAction, QShortcut,QFileDialog, QMenu, QScrollArea, QFrame
from PyQt5.QtGui import QKeySequence, QPixmap, QColor
from PyQt5.QtCore import Qt, QRect

from package.DraggableScrollArea import DraggableScrollArea
from package.clickableLabel import QClickableLabel, QQuickReleaseLabel
from package.photoHandler import photoHandler


class photoGalery(QWidget):
    def __init__(self,superior, photoHandler:photoHandler):
        super().__init__()
        self.superior=superior
        self.photoHandler = photoHandler
        self.allLabels = []
        self.area, self.scrollLay = self.makeScrollArea()
        lay = QHBoxLayout()
        lay.addWidget(self.area)
        self.setLayout(lay)




    

    def loadAllThumbnails(self):
        allThumbs = self.photoHandler.getAllThumbnails()
        self.allLabels = []
        for t in reversed(allThumbs):
            self._addLab(t)
        self.update_pixmap()

    def _addLab(self,path):

        pix = QPixmap(path)
        l = QQuickReleaseLabel()
        l.fileName = os.path.basename(path)
        l.clicked.connect(self.labClicked)
        l.setScaledContents(True)
        l.setPixmap(pix)
        print("added:",path)
        l.setMaximumHeight(self.height()-50)
        self.allLabels.append(l)
        self.scrollLay.insertWidget(0,l)

    def addThumbnail(self,filename):
        p =self.photoHandler.getThumbnail(filename)
        self._addLab(p)
        self.update_pixmap()



    def labClicked(self):
        fileName = self.sender().fileName
        self.superior.newImageClicked(fileName)
    def resizeEvent(self, event):
        """Override the resize event to update the QLabel's pixmap size dynamically."""
        self.update_pixmap()
        super().resizeEvent(event)

    def update_pixmap(self):

        # Get the current size of the window (or parent container)
        
        container_height = self.superior.height()

        #Label bekommt 18%
        labHeight = int(container_height*0.15)
        pixmap_width , pixmap_height = self.photoHandler.nativeRes
        aspect_ratio = pixmap_width / pixmap_height
       
        new_height = labHeight
        new_width = int(new_height * aspect_ratio)


        for l in self.allLabels:
            l.setFixedSize(new_width, new_height)
    
    def makeScrollArea(self):
        scrollArea = DraggableScrollArea(self)
        scrollArea.setGeometry(QRect(10,60,580,300))
        scrollArea.setAutoFillBackground(True)
        pal = scrollArea.palette()
        pal.setColor(scrollArea.backgroundRole(), QColor(255,255,255))
        scrollArea.setPalette(pal)
        scrollArea.setFrameShape(QFrame.StyledPanel)
        scrollArea.setLineWidth(1)
        scrollArea.setWidgetResizable(True)

        container = QWidget()
        scrollArea.setWidget(container)
        
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff )
        scrollGrid = QHBoxLayout()
        

        container.setLayout(scrollGrid)
        return [scrollArea, scrollGrid]
    
    

