# Simple Photo Booth

Hello. This is a very simple photo booth i designed quick and dirty (~5h of work). It was aimed for a wedding for those who do not want to rent the very expensive photo boxes. It is designed for Windows, as it uses the windows print service. If you want to run it on a linux based system (especially on a Raspberry Pi), there are way better options out there for you.

Please do not view this as a finished product. It worked very well for one night and I thought that others might want to find parts of it helpful.

## What it does
It grabs the live-stream of a webcam to display. It uses a snapshot of it and saves it as a picture. This picture is then printed onto a photo printer if the user wishes so.
Every picture is stored and can be printed at a later time as well. The interface is minimalistic and was easily understood by the guests. It is designed for a touch screen. You might want to change the resolution of some of the elements.

It worked very great with a smartphone camera as a webcam. I used https://iriun.com/ with a Samsung Fold 3. The goal was to produce nice looking printed photos, not files with the best possible Quality.

## What you need (hardware)
- Windows PC with touchscreen (I used a Surface)
- Webcam (or smartphone camera)
- Printer (I used the Canon SELPHY CP1500) (If you use a different one, please change the name in package/printerHandler.py. At some point it will not be hardcoded anymore)

## What you need (software)
- Python 3.9 (propably works with other versions too)
- PyQt5
- cv2
- win32
- pywintypes
- Pillow

## Known Issues
- Multiple prints in a row are possible. This clogs up the printer queue and might cause problems. 
- AI Generated icons are bad. But I do not want to design them myself.
- If the printer is set to vertical, it will print only half the image. 

## Plan for this Project
I will update it at some time for a future wedding I attend. Until then i propably cannot be bothered to. If you want to use it, please feel free to use it any way you want under the Apache 2.0 license.