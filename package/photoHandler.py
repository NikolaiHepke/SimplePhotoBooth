import os
import sys
import time
from PyQt5.QtCore import pyqtSignal,QObject, QThreadPool
import uuid
import cv2
import glob

from PyQt5.QtCore import QRunnable, QThreadPool, pyqtSignal, QObject
from package.Runnable import Runnable
from package.fileHandler import fileHandler

class photoHandler(QObject):
    nativeRes = [1620, 1080]
    OnNewThumbNail = pyqtSignal(str)
    def __init__(self, fileHan):
        
        self.fileHandler = fileHan
        self.thumbnailFolder = r"Thumbnails"

        super().__init__()
        os.makedirs(self.getQuarterDir(),exist_ok=True)
        os.makedirs(self.getEigthDir(),exist_ok=True)
        os.makedirs(self.getSixteenthDir(),exist_ok=True)

        self.allImages= {}
        self.threadpool = QThreadPool()
        self.lookForImages()

    def lookForImages(self):
        #prüfe, ob die Bilder alle da sind
        images = [f.path for f in os.scandir(self.fileHandler.aimFolder)]
        print(len(images))
        toThumbnail = []
        for img in images:
            if not self.checkForThumbnail(img):
                toThumbnail.append(img)

        print("noThumb: ", toThumbnail)

        self.makeThumbnails(toThumbnail)



    def getNewUniqueFileName(self):
        extension = "jpg"
        while True:
            # Create a unique identifier
            unique_name = str(uuid.uuid4())
            
            # Create the full file path with the given extension
            filename = f"{unique_name}.{extension}"
            filepath = os.path.join(self.fileHandler.aimFolder, filename)
            
            # Check if the filename already exists
            if not os.path.exists(filepath):
                return filepath
        
    def checkForThumbnail(self, path):
        return os.path.exists(os.path.join(self.getQuarterDir(), os.path.basename(path)))
           
    def getQuarterDir(self):
        return os.path.join(self.thumbnailFolder, "quarter")
    
    def getEigthDir(self):
        return os.path.join(self.thumbnailFolder, "eigth")
    
    def getSixteenthDir(self):
        return os.path.join(self.thumbnailFolder, "sixteenth")
    

    def getThumbnail(self,filename):
        return os.path.join(self.getQuarterDir(), filename)
    

    def getAllThumbnails(self):
        #order by creation date of original
        originals = [f.path for f in os.scandir(self.getQuarterDir()) ]
        sortedFiles = sorted(originals, key=os.path.getctime,reverse=True)
        thumbnails = [os.path.join(self.getQuarterDir(),os.path.basename(f)) for f in sortedFiles]
        return thumbnails


    def makeThumbnails(self, paths):
   
        params = [self.nativeRes, self.getQuarterDir(), self.getEigthDir(), self.getSixteenthDir()]
        pathsWithParams = [[path]+ params for path in paths]
        
        for p in pathsWithParams:
            print(p)
            runner = Runnable(self._makeThumbnail, p)
            runner.signals.result.connect(self.OnNewThumbNail.emit)
            self.threadpool.start(runner)

        
        
#        print(results)



    def _makeThumbnail(self,signals,params):
        try:
            # Load just once, then successively scale down
            filename, nativeRes, quaterDir, eigthDir, sixteenthDir = params
            im = cv2.imread(filename)
            im = im[:,:1620]
            quater = cv2.resize(im, (int(nativeRes[0]/4),int(nativeRes[1]/4)))
            
            cv2.imwrite(os.path.join(quaterDir,os.path.basename(filename)), quater) 
            eigth = cv2.resize(im, (int(nativeRes[0]/8),int(nativeRes[1]/8)))
            cv2.imwrite(os.path.join(eigthDir,os.path.basename(filename)), eigth) 
            sixteenth = cv2.resize(im, (int(nativeRes[0]/16),int(nativeRes[1]/16)))
            cv2.imwrite(os.path.join(sixteenthDir,os.path.basename(filename)), sixteenth) 
            
            return os.path.basename(filename)
        except Exception as e: 
            #raise e
        
            return e 




