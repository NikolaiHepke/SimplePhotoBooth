from PyQt5.QtWidgets import QApplication
import package.mainWindow as mainW
import sys


def start():


    app = QApplication(sys.argv)
    m = mainW.mainWindow(app)
    
    
    sys.exit(app.exec_())  
  
       # m.close()
    




start()