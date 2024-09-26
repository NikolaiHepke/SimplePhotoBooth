import math
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton
from PyQt5.QtCore import QTimer,QSize
from PyQt5.QtGui import QImage, QPixmap, QKeyEvent,QIcon
import cv2

from package.camera import camera
from package.clickableLabel import QClickableLabel
from package.overlayLabelClick import overlayLabelClick
from package.photoHandler import photoHandler

class photoboothMode(QWidget):
    closeIcon = r"assets/close.png"
    def __init__(self,superior, photoHandler:photoHandler):
        super().__init__()
        self.timeTillAccept=10
        self.superior = superior
        self.photoHandler = photoHandler
        self.camera = camera()
        
        self.initWindow()

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateFrame)
        self.msPerUpdate = 30
        self.timer.start(self.msPerUpdate) 

        self.countdownTimer = 0
        self.countDownSet = False
        self.startCounterTime = 5

        self.imageToPrint  = None
        self.showMaximized()

        
        

    def initWindow(self):
        self.lay = QVBoxLayout()


        #Control Elements
        self.camComb = QComboBox()
        self.camComb.addItems(camera.list_windows_video_devices())
        self.camComb.currentIndexChanged.connect(self.currentCamChanged)

        self.setDefaultBtn = QPushButton("Als Standard festlegen")
        self.setDefaultBtn.clicked.connect(self.setDefault)

        self.closeBtn = QPushButton("")
        self.closeBtn.setIcon(QIcon(self.closeIcon))
        self.closeBtn.setIconSize(QSize(100,100))
        self.closeBtn.clicked.connect(self.close)
        self.topLay = QHBoxLayout()
        self.topLay.addWidget(self.camComb)
        self.topLay.addWidget(self.setDefaultBtn)
        self.topLay.addStretch(4)
        self.topLay.addWidget(self.closeBtn)
        self.lay.addLayout(self.topLay)

    
        self.display = QClickableLabel()
        self.display.clicked.connect(self.startCountDown)
        self.display.setScaledContents(True)    
        self.lay.addWidget(self.display)
        self.setLayout(self.lay)
       
    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        if(key in [16777330,16777220]):
            self.startCountDown()
        

    def closeEvent(self,ev):
        self.superior.photoBoothStopped()
        self.camera.close()
        

    def updateFrame(self):
        success ,frame = self.camera.snap()
        self.countdownTimer -= (self.msPerUpdate/ 1000)
        if(self.countDownSet and self.countdownTimer <= 0):
            self.countDownDone()
            return

        if success:
            # Convert the frame from BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            
            if(not self.countDownSet):
                self.writeText(frame_rgb)
            else:
                self.writeTimer(frame_rgb)


            # Convert the frame to QImage
            height, width, channel = frame_rgb.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.display.setPixmap(QPixmap.fromImage(q_image))


            # Set the QImage to the QLabel

    def writeText(self,frame):
        text = "Na ihr tollen Menschen?\nKlickt hier!!!!\nSmiiiile!!!"
        font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX  # Choose a font
        font_scale = 3  # Large font scale for big text
        color = (255, 255, 255)  # Green color for the text (BGR format)
        thickness = 3  # Thickness of the text
        
        self.draw_centered_text(frame, text, font, font_scale, color, thickness, 1.5)


    def writeTimer(self,frame):
        text = "{}".format(math.ceil(self.countdownTimer))
        font = cv2.FONT_HERSHEY_DUPLEX  # Choose a font
        font_scale = 10  # Large font scale for big text
        color = (255, 255, 255)  # Green color for the text (BGR format)
        thickness = 3  # Thickness of the text
        frame_height, frame_width, _ = frame.shape
        
        self.draw_centered_text(frame, text, font, font_scale, color, thickness, 1)
        self.draw_partial_circle(frame,self.countdownTimer / self.startCounterTime, color)

    def draw_partial_circle(self,image,   fraction, color):
        thickness = 5 
        # Calculate the angle that corresponds to the percentage
        # Full circle = 360 degrees, so percentage of that is:
        radius = 300
        angle_extent = int(360 * fraction )
        center = self.camera.getCenter()
        # Draw the partial circle (using angles in degrees)
        # The full circle is from 0 to 360 degrees, so we draw from 0 to `angle_extent`
        cv2.ellipse(image, center, (radius, radius), 0, 0, angle_extent, color, thickness)
    
    def applyControlElements(self):
        #bastle ein Overlay für löschen oder Audrucken!
        w = self.display.width()//2
        h = self.display.height()
        self.contBtn = overlayLabelClick(self,"Weiter", w, h,self.timeTillAccept)
        self.printBtn = overlayLabelClick(self,"Drucken", w,h)
        self.contBtn.setParent(self)
        self.printBtn.setParent(self)
        self.contBtn.move(self.display.pos().x(),self.display.pos().y())
        self.printBtn.move(self.display.pos().x()+w,self.display.pos().y())

        self.contBtn.clicked.connect(self.continueWithCam)
        self.printBtn.clicked.connect(self.printCurrentImg)

        self.contBtn.setVisible(True)
        self.printBtn.setVisible(True)
        print("Display")



    def countDownDone(self):
        #fange ein Bild ein
        success = False
        while not success:
            success,frame = self.camera.snap()
            if(success):
                savePath = self.photoHandler.getNewUniqueFileName()
                cv2.imwrite(savePath, frame)
                self.superior.newImageTaken(os.path.basename(savePath))
                self.imageToPrint = savePath

        #Höre auf zu aktualisieren
        self.timer.stop()
        #schreibe Bild in das Label
        self.display.setPixmap(QPixmap(savePath))
        
        self.countDownSet = False
        self.applyControlElements()



    def draw_centered_text(self,frame, text, font, font_scale, color, thickness, line_height_factor):
        lines = text.split('\n')  # Split the text into lines
        frame_height, frame_width, _ = frame.shape

        
        # Find the total height of the text block (considering line breaks)
        total_text_height = 0
        line_sizes = []
        for line in lines:
            (text_width, text_height), baseline = cv2.getTextSize(line, font, font_scale, thickness)
            line_sizes.append((text_width, text_height))
            total_text_height += int(text_height * line_height_factor)
            
        
        # Calculate starting y position (so the text block is vertically centered)
        y_offset = (frame_height - total_text_height) // 2
        

        # Draw each line of text, centered horizontally
        for i, line in enumerate(lines):
            text_width, text_height = line_sizes[i]
            x_offset = (frame_width - text_width) // 2  # Center the text horizontally
            y_offset += text_height # Move down the height of the line

            cv2.putText(frame, line, (x_offset, y_offset), font, font_scale, color, thickness, cv2.LINE_AA)
            y_offset += int(text_height * (line_height_factor - 1))  # Add space between lines

    def startCountDown(self):
        self.countDownSet = True
        self.countdownTimer =self.startCounterTime

    def currentCamChanged(self, newIndex):
        self.camera.changeCamera(newIndex)

    def setDefault(self):
        self.camera.setNewDefault(self.camComb.currentIndex())


    def continueWithCam(self):
        print("continue")
        self.contBtn.killTimers()
        self.printBtn.killTimers()
        self.contBtn.setParent(None)
        self.printBtn.setParent(None)
        self.timer.start()

    def printCurrentImg(self):
        print("print")
        self.superior.printImage(self.imageToPrint)
        self.continueWithCam()