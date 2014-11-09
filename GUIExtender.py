from PySide import QtGui, QtCore
from GUI import Ui_MainWindow
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import FourierSeries as fs
import os
import StringValidator as sv
import Parseval as pt
from math import pi
import Orthogonality as O

class MplCanvas(FigureCanvas):
    """
    Creates a default canvas to be embedded into the GUI.
    """
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class DynamicMplCanvas(MplCanvas):
    """
    Creates a matplotlib canvas which can be used to embed matplotlib plots into
    the GUI.
    """
    def __init__(self, *args, **kwargs):
        MplCanvas.__init__(self, *args, **kwargs)

    def update_figure(self, coordinates, title, xlabel, ylabel, legend, location, xlim, ylim):
        """
        Takes a list of a list of coordinate pairs and plots them on the same
        plot.
        """
        #Not sure how to handle ticks yet...
        self.axes.clear()
        self.axes.grid()
        fsize = "10"

        for coordinate in coordinates:
            self.axes.plot(coordinate[0], coordinate[1])
            self.axes.set_title(title, fontsize=fsize)
            self.axes.set_xlabel(xlabel, fontsize=fsize)
            self.axes.set_ylabel(ylabel, fontsize=fsize)
            self.axes.legend(legend, loc=location, fontsize=fsize)
            self.axes.set_xlim(xlim)
            self.axes.set_ylim(ylim)

        self.draw()
        self.show()

    def save_plot(self, file_name):
        images = "user-images"
        if not os.path.exists(images) and not os.path.isdir(images):
            os.makedirs(images)

        self.fig.savefig(os.path.join(images, file_name))

class GUIExtender(Ui_MainWindow):
    """
    This class extends the automatically generated GUI created by PySide.  It
    should be used to wire up the signals and slots so that the GUI and
    functionality talk to each other.

    It is used to initialise the default state of the GUI, ready for the user.

    It inherits from Ui_MainWindow which is automatically generated code, by
    doing this any changes made to the UI will not subsequently erase any of the
    extended code, allowing for more flexibility.
    """

    def connect_signals_and_slots(self):
        """
        Ties up the signals and slots sent by the Qt interface to the program
        logic.
        """
        # Orthogonality
        self.orthogonality_m.sliderReleased.connect(self.calc_integral)
        self.psi_psi.clicked.connect(self.calc_integral)
        self.psi_phi.clicked.connect(self.calc_integral)
        self.phi_phi.clicked.connect(self.calc_integral)

        # Fourier series
        self.function_selector.currentIndexChanged.connect(self.select_function)
        self.number_of_terms.sliderReleased.connect(self.change_terms)
        self.save.clicked.connect(self.save_file)
        self.fs_checkbox.stateChanged.connect(self.select_function)

        #Parseval's Theorem
        self.number_of_terms_pi.sliderReleased.connect(self.approximate_pi)
        self.parseval_save.clicked.connect(self.save_file)

    def calc_integral(self):
        m = self.orthogonality_m.value()

        selected = ""

        if self.psi_psi.isChecked():
            selected = "psi_psi"
        elif self.psi_phi.isChecked():
            selected = "psi_phi"
        else:
            selected = "phi_phi"

        self.orth = O.Orthogonality(selected)

        integrals = self.orth.inner_product(m, pi)
        n = 0
        text = ""

        for integral in integrals:
            text += "When n = %s and m = %s the integral is: %.3f \n" % (n, m, abs(integral))
            n += 1

        self.integral_text.setPlainText(text)
        self.m_label.setText(QtGui.QApplication.translate(
                                                "MainWindow",
                                                "m = %s" % m,
                                                None,
                                                QtGui.QApplication.UnicodeUTF8))

    def approximate_pi(self):
        self.pt = pt.Parseval()
        n = self.number_of_terms_pi.value()
        self.mplCanvas = DynamicMplCanvas(self.par_widget, width=7, height=5, dpi=100)
        self.number_n_pi.setText(QtGui.QApplication.translate(
                                                "MainWindow",
                                                "n = %s" % n,
                                                None,
                                                QtGui.QApplication.UnicodeUTF8))
        x, y = self.pt.plot_pi(n)
        self.computed_pi.setText(QtGui.QApplication.translate(
                                                "MainWindow",
                                                "The computed value of pi is:\n %s" % self.pt.compute_pi(n),
                                                None,
                                                QtGui.QApplication.UnicodeUTF8))

        title = r"Approximation of $\pi$ as $n\rightarrow\infty$"
        legend = [r"Approximation of $\pi$ as $n\rightarrow\infty$", r"A line to show the value of $\pi$"]
        ylabel = r"Number of terms to calculate $\pi$, $\left(n\right)$"
        xlabel = r"An approximation of $\pi$"
        location = "upper left"
        xlim = [2.4, pi+0.2]
        ylim = [0, y[-1]+1]

        self.mplCanvas.update_figure([(x, y), ([pi, pi], [0, n])], title, xlabel, ylabel, legend, location, xlim, ylim)

    def select_function(self):
        n = self.number_of_terms.value()
        function = self.function_selector.currentIndex()
        self.update_canvas(function, n)

    def change_terms(self):
        n = self.number_of_terms.value()
        function = self.function_selector.currentIndex()
        self.number_of_terms_label.setText(QtGui.QApplication.translate(
                                                "MainWindow",
                                                "n = %s" % n,
                                                None,
                                                QtGui.QApplication.UnicodeUTF8))
        self.update_canvas(function, n)

    def update_canvas(self, function, n):
        self.fs = fs.FourierSeries()
        self.mplCanvas = DynamicMplCanvas(self.widget, width=7, height=4.5, dpi=100)

        function_name = self.function_selector.currentText()
        title = r"An approximation of the %s using the Fourier series with %s terms." % (function_name, n)
        xlabel = r"The values of x"
        ylabel = r"The values of y"
        legend = [r"%s" % function_name]
        location = "upper right"
        xlim = []
        ylim = []

        x, y = [], []
        fsx, fsy = [], []

        if function == 0:
            x, y = self.fs.calc_triangle()
            if self.fs_checkbox.isChecked():
                fsx, fsy = self.fs.fs_calc_triangle(n)
                legend.append(r"Fourier series approximation")
            xlim = [-0.2, 2.2]
            ylim = [-1.2, 1.2]
        elif function == 1:
            x, y = self.fs.calc_square()
            if self.fs_checkbox.isChecked():
                fsx, fsy = self.fs.fs_calc_square(n)
                legend.append(r"Fourier series approximation")
            xlim = [-.5, 2*pi+1]
            ylim = [-1.5, 1.5]
        else:
            x, y = self.fs.calc_saw()
            if self.fs_checkbox.isChecked():
                fsx, fsy = self.fs.fs_calc_saw(n)
                legend.append(r"Fourier series approximation")
            location = "upper left"
            xlim = [-0.2, 2 * pi + 0.2]
            ylim = [-0.2, pi + 0.2]

        self.mplCanvas.update_figure([(x, y), (fsx, fsy)], title, xlabel, ylabel, legend, location, xlim, ylim)

    def initial_canvas(self):
        self.mplCanvas = DynamicMplCanvas(self.widget, width=7, height=4.5, dpi=100)
        self.update_canvas(0, 1)

    def inital_text(self):
        
        path = os.getcwd()
        orth = os.path.join(path, "latex/Orthogonality.pdf")
        fourier = os.path.join(path, "latex/Orthogonality.pdf")
        parseval = os.path.join(path, "latex/Orthogonality.pdf")
        
        self.orth_webView.load(QtCore.QUrl(orth))
        self.orth_webView.show()
        
        self.fourier_webView.load(QtCore.QUrl(fourier))
        self.fourier_webView.show()
        
        self.parseval_webView.load(QtCore.QUrl(parseval))
        self.parseval_webView.show()
         
        #Unfortunatley having to load images instead of pdfs as the QWebView 
        # isn't reliable in loading pdfs and it has flaky MathJax support.
        """path = os.getcwd()
        orth = os.path.join(path, "orthogonality.jpg")       
        fourier = os.path.join(path, "fourier.jpg")
        parseval = os.path.join(path, "parseval.jpg")
        
        scene = QtGui.QGraphicsScene()
        scene.addPixmap(QtGui.QPixmap(QtGui.QImage(orth)))
        self.orth_graphicsView.setScene(scene)
        self.orth_graphicsView.centerOn(QtCore.QPointF(0,0))
        self.orth_graphicsView.show()
        
        scene2 = QtGui.QGraphicsScene()
        scene2.addPixmap(QtGui.QPixmap(fourier))
        self.fourier_graphicsView.setScene(scene2)
        self.fourier_graphicsView.centerOn(QtCore.QPointF(0,0))
        self.fourier_graphicsView.show()
        
        scene3 = QtGui.QGraphicsScene()
        scene3.addPixmap(QtGui.QPixmap(parseval))
        self.parseval_graphicsView.setScene(scene3)
        self.parseval_graphicsView.centerOn(QtCore.QPointF(0,0))
        self.parseval_graphicsView.show()"""

    def initialise(self):
        self.inital_text()
        self.initial_canvas()
        self.psi_psi.setChecked(True)
        self.approximate_pi()
        self.calc_integral()

    def save_file(self):
        filename = self.filename.text()

        if filename == "":
            filename = self.function_selector.currentText().replace(" ", "_") + "_" + str(self.number_of_terms.value())
            self.mplCanvas.save_plot(filename)
            self.validation.setText("File saved.")
        else:
            validator = sv.StringValidator(filename)
            if not validator.isAlphaNumeric():
                self.validation.setText(QtGui.QApplication.translate(
                                                "MainWindow",
                                                "Alphanumeric characters only!",
                                                None,
                                                QtGui.QApplication.UnicodeUTF8))
            else:
                self.mplCanvas.save_plot(filename)
                self.validation.setText("File saved.")
