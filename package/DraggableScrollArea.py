

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt5.QtCore import Qt, QPoint,QTimer

class DraggableScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setMouseTracking(True)
        self.dragging = False
        self.last_pos = QPoint()

        # Variables to track momentum
  
        self.velocity = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.apply_momentum)
        self.deceleration = 0.95  # The rate at which velocity decreases
        self.min_velocity = 1  #

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("startDrag")
            self.dragging = True
            self.last_pos = event.pos()
          
            self.timer.stop()
            self.setCursor(Qt.ClosedHandCursor)  # Change cursor to indicate dragging
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.dragging:
            # Calculate the delta of the mouse movement
            delta = event.pos() - self.last_pos
            self.velocity = delta.x()
            self.last_pos = event.pos()
            print("velo",self.velocity)
            # Adjust the scrollbars based on the mouse movement
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            #self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            
            self.timer.start(16)
          
            self.last_pos = None
            self.setCursor(Qt.ArrowCursor)  # Reset cursor after releasing
 
        super().mouseReleaseEvent(event)

    def apply_momentum(self):
        print("momentum",self.velocity)
        # Apply the momentum to the scroll bars

        self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - self.velocity)

        # Apply deceleration
        self.velocity *= self.deceleration

        # Stop scrolling when velocity is small
        if abs(self.velocity) < self.min_velocity :
            self.timer.stop()
            print("stop")


    def wheelEvent(self, event):
       
        """Override the wheelEvent to enable horizontal scrolling."""
        
        delta = event.angleDelta().y()  # Get vertical scroll delta
        self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta)