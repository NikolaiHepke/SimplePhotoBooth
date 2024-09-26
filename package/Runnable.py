from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject
import traceback, sys

#https://www.pythonguis.com/tutorials/multithreading-pyqt-applications-qthreadpool/
class Runnable(QRunnable):
    finished =pyqtSignal()
    def __init__(self, function, *args):
        super().__init__()
        self.function = function
        self.args = args
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        self.signals.started.emit()
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.function(self.signals,*self.args)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

class WorkerSignals(QObject):
    started = pyqtSignal()
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    message = pyqtSignal(str)
    progress = pyqtSignal(int)
    maxSignal= pyqtSignal(int)