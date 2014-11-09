import sys
import os
from PySide import QtCore, QtGui, QtWebKit #@UnusedWildImport

class DialogTest(QtGui.QDialog):
    def __init__(self, parent = None):
        super(DialogTest, self).__init__(parent)
        self.resize(620, 600)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.PreviewBox = QtWebKit.QWebView()   
        self.PreviewBox.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)
        self.PreviewBox.settings().setAttribute(QtWebKit.QWebSettings.WebAttribute.DeveloperExtrasEnabled, True)
        self.PreviewBox.settings().setAttribute(QtWebKit.QWebSettings.PrivateBrowsingEnabled, True)
        self.PreviewBox.settings().setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessRemoteUrls, True)
        self.PreviewBox.loadFinished.connect(self._loadfinished)
        self.button_test1 = QtGui.QPushButton("File 1")
        self.button_test1.clicked.connect(self._onselect1)
        self.button_test2 = QtGui.QPushButton("File 2")
        self.button_test2.clicked.connect(self._onselect2)
        layout_Buttons = QtGui.QHBoxLayout()        
        layout_Buttons.addWidget(self.button_test1)        
        #layout_Buttons.addStretch()
        layout_Buttons.addWidget(self.button_test2) 
        layout_Main = QtGui.QVBoxLayout()      
        layout_Main.addLayout(layout_Buttons)  
        layout_Main.addWidget(self.PreviewBox)                  
        self.setLayout(layout_Main)      
    def Execute(self):
        self.show()
        self.exec_()
    def _onselect1(self):
        path = os.path.join(os.getcwd(), "fourier.pdf")
        print path
        self.PreviewBox.load(QtCore.QUrl().fromLocalFile(path))
    def _onselect2(self):
        self.PreviewBox.load(QtCore.QUrl().fromLocalFile("c:\\tmp\\test2.pdf"))
    def _loadfinished(self, ok):
        #self.PreviewBox.repaint()
        pass
app = QtGui.QApplication(sys.argv)
DialogTest().Execute() 