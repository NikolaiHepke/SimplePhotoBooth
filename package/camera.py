import os
import cv2
import subprocess
import json

class camera:
    confPath = "Config/cameraConfig.json"
  
    def __init__(self):
        self.loadDefaults()
        print("InitCam")
        self.cap = cv2.VideoCapture(self.defaultCamera) # video capture source camera (Here webcam of laptop) 
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.camWidth)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camHeight)
        

    def changeCamera(self,newId):
        self.cap.release()
        self.cap = cv2.VideoCapture(newId) # video capture source camera (Here webcam of laptop) 
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.camWidth)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camHeight)

    def close(self):
        self.cap.release()

    def setNewDefault(self, newId):
        self.defaultCamera = newId
        self.saveDefaults()
    def snap(self):
        if(self.cap.isOpened()):
            ret, frame = self.cap.read()
            frame = frame[:,:self.printWidth]
            return ret,frame
        return False,False
    
    def getCenter(self):
        return (self.printWidth//2, self.printHeight//2)
    
    def list_windows_video_devices():
        devices = []
        result = subprocess.run(['ffmpeg', '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy'], stderr=subprocess.PIPE, text=True)
        for line in result.stderr.split('\n'):
            if "DirectShow video devices" in line:
                break
        for line in result.stderr.split('\n'):
            if "dshow" in line and "video" in line:
                devices.append(line.strip().split('"')[1])
        
        return devices
    
    def _loadDefaultConfig(self):
        self.defaultCamera = 0
        self.camWidth = 1920
        self.camHeight =1080
        self.printWidth= 1620
        self.printHeight= 1080

    
    def loadDefaults(self):
        if(os.path.exists(self.confPath)):
            with open(self.confPath, "r") as f:
                dct = json.load(f)
                self.defaultCamera = dct["defaultCamera"]
                self.camWidth = dct["camWidth"]
                self.camHeight = dct["camHeight"]
                self.printWidth= dct["printWidth"]
                self.printHeight= dct["printHeight"]

        else:
            self._loadDefaultConfig()
            self.saveDefaults()

    def saveDefaults(self):
        dct = {}
        dct["defaultCamera"] = self.defaultCamera 
        dct["camWidth"] = self.camWidth 
        dct["camHeight"] = self.camHeight 
        dct["printWidth"] = self.printWidth
        dct["printHeight"] = self.printHeight
        os.makedirs(os.path.dirname(self.confPath),exist_ok=True)
        with open(self.confPath, "w+") as f:
            json.dump(dct,f)
if __name__ == "__main__":
    print(camera.list_windows_video_devices())