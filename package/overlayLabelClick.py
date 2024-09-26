from package.clickableLabel import QClickableLabel


from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtGui import QImage, QPixmap,QColor,QPainter, QPen, QFont,QBrush

class overlayLabelClick(QClickableLabel):
    def __init__(self,superior, text, width, height, timeTillAccept=-1):
        self.baseColor = QColor(255,255,255)
        #durchsichtig
        self.superior = superior
        super().__init__()
        self.w, self.h = width, height
        self.dispText = text
        self.timeTillAccept = timeTillAccept
        
        self.currentTime = 0
        
        if(self.timeTillAccept != -1):
            self.timer = QTimer()
            self.timer.timeout.connect(self.updateTimer)
    
            self.msPerUpdate = 50
            self.timer.start(self.msPerUpdate)       

        self.background= self.createBackground()
        
        self.setPixmap(self.background)
        self.setFixedSize(width,height)

        self.clicked.connect(self.killTimers)
    
    def createBackground(self):
        pix = QPixmap(self.w,self.h )

        #Grundfarbe
        
        self.baseColor.setAlpha(100)
        pix.fill(self.baseColor)

        #Zeichner vorlegen
        self.baseColor.setAlpha(255)
        painterInstance = QPainter(pix)
        pen = QPen(self.baseColor)
        pen.setWidth(10)
        painterInstance.setPen(pen)
        #Rahmen
        painterInstance.drawRect(0,0,self.w, self.h)
        #ProgressBox
        toKill = False
        if(self.timeTillAccept != -1):
            #male eine Kiste
            
            progress = (self.currentTime / self.timeTillAccept) 
            if(progress  >= 1):
                toKill = True
                progress = 1    
            alpha = 100 + int(progress * 155)
            self.baseColor.setAlpha(alpha)
            brush = QBrush(self.baseColor)
            
            painterInstance.setPen(Qt.NoPen)
            painterInstance.setBrush(brush)
            
            painterInstance.drawRect(0,0,int(self.w*progress),self.h)
            self.baseColor.setAlpha(255)

            pen = QPen(self.baseColor)
            pen.setWidth(10)
            painterInstance.setPen(pen)
            painterInstance.setBrush(Qt.NoBrush)

        #Text
        font = QFont("Arial", 30, QFont.Bold)
        painterInstance.setFont(font)
        painterInstance.drawText(pix.rect(), Qt.AlignVCenter | Qt.AlignHCenter, self.dispText)

        painterInstance.end()
        if(toKill):
            self.clicked.emit()
          
            

        return pix
    

    def updateTimer(self):
        #Update den hitnergrund
        self.currentTime += self.msPerUpdate/1000
        self.background= self.createBackground()
        
        self.setPixmap(self.background)  


    def killTimers(self):#
        if(self.timeTillAccept != -1):
            self.timer.stop()