import os
import shutil
import time
from PyQt5.QtCore import pyqtSignal,QObject, QThreadPool
from win32 import win32file,win32api
import pywintypes
import winerror
from package.Runnable import Runnable, WorkerSignals
class fileHandler(QObject):
    transferDone = pyqtSignal(int)
    ejectError = pyqtSignal(str, int)
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()

        self.sourceFolder = r"D:\Files"

        self.aimFolder = "AimFolder"
        os.makedirs(self.aimFolder,exist_ok=True)
        #self.startLookingForFiles()
        


    def startLookingForFiles(self):
        self.keepLooking=True
        r = Runnable(self.findAndCopyFiles)
        r.signals.message.connect(self.newPictureAvailable)
        self.threadpool.start(r)

    def newPictureAvailable(self,path):
        print(path)

    def killThread(self):
        self.keepLooking = False

    def eject_drive(self):
        drive_letter = self.sourceFolder[0]
        drive_letter = drive_letter.upper() + ':\\'
        try:
            # Attempt to open the volume
            volume = win32file.CreateFile(
                drive_letter,
                win32file.GENERIC_READ,
                win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE,
                None,
                win32file.OPEN_EXISTING,
                0,
                None
            )
            
            # Try to dismount the volume
            dismount_result = win32file.DeviceIoControl(volume, win32file.FSCTL_DISMOUNT_VOLUME, None, 0)
            if not dismount_result:
                msg = f"Failed to dismount {drive_letter}. It might be in use."
                print(msg)
                return False, msg
            
            # Try to eject the media
            eject_result = win32file.DeviceIoControl(volume, win32file.IOCTL_STORAGE_EJECT_MEDIA, None, 0)
            if eject_result:
                msg = f"Device {drive_letter} ejected successfully."
                print(msg)
                return True,msg
            else:
                msg = f"Failed to eject device {drive_letter}."
                print(msg)
                return False,msg
            
        except pywintypes.error as e:
            if e.winerror == win32file.ERROR_DEVICE_IN_USE:
                msg = f"Cannot eject {drive_letter} because it is in use."
                print(msg)
            else:
                msg = f"An error occurred: {e}"
                print(msg)
            return False,msg
        finally:
            # Ensure the handle is closed
            try:
                win32api.CloseHandle(volume)
            except Exception as e:
                msg = f"Failed to close the handle: {e}"
                print(msg)
                return False,msg

    def findAndCopyFiles(self,signals:WorkerSignals):
        # in thread!!
        while self.keepLooking:
            #prüfe, ob Ordner existiert
            if(os.path.exists(self.sourceFolder)):
                #falls ja, schnappe alle Dateien (die SD Karte ist dismounted, also muss es passen!)
                allFiles = os.listdir(self.sourceFolder)
                print(allFiles)

                for file in allFiles:
                    aim= os.path.join(self.aimFolder,file)
                    source = os.path.join(self.sourceFolder,file)
                    
                    shutil.move(source,aim )
                #wenn alle Daten drüben sind, dismounte die SD Karte
                success, msg = self.eject_drive()
                if(success):
                #informiere den main Thread
                    self.transferDone.emit(len(allFiles))
                else:
                    #gebe Fehlermeldung zurück
                    self.ejectError(len(allFiles),msg)
                    
            time.sleep(0.5)

        print("Thread ended gracefully")
    
  