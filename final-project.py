from PySide import QtGui
from GUIExtender import GUIExtender
import sys

def main():
    """
    Launches the GUI interface for the Fourier series approximator.
    """  
    #makes it runnable in Canopy but wont be fixed as PySide dev do not think it
    #is a real bug.  Canopy will still report an error:
    #    An exception has occurred, use %tb to see the full traceback.
    #     SystemExit: -1


    app=QtGui.QApplication.instance() # checks if QApplication already exists 
    if not app: # create QApplication if it doesnt exist 
        app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = GUIExtender()
    ui.setupUi(MainWindow)
    ui.connect_signals_and_slots()
    ui.initialise()
    MainWindow.show()
    sys.exit(app.exec_())

main()
