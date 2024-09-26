from datetime import datetime
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal


class QClickableLabel(QLabel):
  clicked=pyqtSignal()
  def __init__(self,superior=None):
    
    super().__init__(superior)

  def mousePressEvent(self, ev):
      self.clicked.emit()
      super().mousePressEvent(ev)


class QQuickReleaseLabel(QLabel):
    clicked=pyqtSignal()
    def __init__(self,superior=None):
      
      super().__init__(superior)

    def mousePressEvent(self, ev):
        self.lastClick = datetime.now()
        super().mousePressEvent(ev)

    def mouseReleaseEvent(self, ev):
       holdTime = datetime.now() - self.lastClick
       if(holdTime.total_seconds() < 0.2):
          self.clicked.emit()
       super().mouseReleaseEvent(ev)
       