import subprocess
import win32print,win32ui
from PIL import Image, ImageWin
import os



class printerHandler:
    printer_name='Canon SELPHY CP1500 (Kopie 1)'
    def __init__(self):
        self.is_printer_available()
        pass


    def print_photo_with_dialog(self,image_path):
        try:
            
            os.startfile(image_path, 'print')
            return True
            
        except Exception as e:
            print(f"Failed to print the image: {e}")
            return False
        

    def printImage(self,imagePath):
        print("prinHan", imagePath)
        
        self._print_photo_windows( imagePath )
    def _print_photo_windows(self, image_path ):
        hprinter = win32print.OpenPrinter(self.printer_name)
        try:
            # Start the print job
            hdc = win32ui.CreateDC()
            hdc.CreatePrinterDC(self.printer_name)
            
            # Open the image using PIL
            print(image_path)
            img = Image.open(image_path)
            #if img.size[0] > img.size[1]:
            #    img = img.rotate(270)
            # Start the document
            hdc.StartDoc(image_path)
            hdc.StartPage()

            # Prepare the image for printing
            dib = ImageWin.Dib(img)
            dib.draw(hdc.GetHandleOutput(), (0, 0, img.size[0], img.size[1]))

            # End the page and document
            hdc.EndPage()
            hdc.EndDoc()

        except Exception as e:
            raise e
            print(f"Failed to print the image: {e}")
        finally:
            # Close the printer handle
            win32print.ClosePrinter(hprinter)


    def _print_photo_windows_alt(self,image_path, printer_name='Canon SELPHY CP1300'):
        try:
            # Use the built-in print command of Windows
            subprocess.run(['print', '/D:' + printer_name, image_path], check=True)
            print(f"Successfully sent {image_path} to {printer_name}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to print {image_path}: {e}")


    def is_printer_available(self):
        try:
            printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
            printer_name =self.printer_name
            for printer in printers:
                if printer_name in printer[2]:
                    # Get printer status
                    printer_handle = win32print.OpenPrinter(printer_name)
                    printer_info = win32print.GetPrinter(printer_handle, 2)  # Level 2 for detailed info
                    win32print.ClosePrinter(printer_handle)
                    
                    status = printer_info['Status']
                    
                    # Status check
                    if status == 0:
                        print(f"Printer '{printer_name}' is available and ready.")
                        return True
                    else:
                        print(f"Printer '{printer_name}' is not available. Status code: {status}")
                        return False
            print(f"Printer '{printer_name}' not found.")
            return False
        except Exception as e:
            print(f"Error checking printer availability: {e}")
            return False
