import sys
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
from scipy import signal

class SignalPlotting(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # Create subplots to show the signals
        self.fig = Figure(figsize=(width, height), dpi=dpi,tight_layout=True)
        self.axes1 = self.fig.add_subplot(2,2,1)
        self.axes1.set_title("FIR FILTER")
        self.axes1.set_xlabel("Frequency(Hz)")
        self.axes1.set_ylabel("Amplitude(dB)")
        self.axes2 = self.fig.add_subplot(2,2,2)
        self.axes2.set_title("FIR COMB FILTER")
        self.axes2.set_xlabel("Frequency(Hz)")
        self.axes2.set_ylabel("Amplitude(dB)")
        self.axes3 = self.fig.add_subplot(2,2,3)
        self.axes3.set_title("IIR FILTER")
        self.axes3.set_xlabel("Frequency(Hz)")
        self.axes3.set_ylabel("Amplitude(dB)")
        self.axes4 = self.fig.add_subplot(2,2,4)
        self.axes4.set_title("IIR COMB FILTER")
        self.axes4.set_xlabel("Frequency(Hz)")
        self.axes4.set_ylabel("Amplitude(dB)")
        super(SignalPlotting, self).__init__(self.fig)
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # Create an instance of the SignalPlotting class
        self.canva = SignalPlotting(self, width=5, height=4, dpi=100)
        # create a flexible layout
        centralWidget = QtWidgets.QWidget()
        layout_vertical = QtWidgets.QVBoxLayout()
        centralWidget.setLayout(layout_vertical)
        check_layout = QtWidgets.QVBoxLayout()
        sliders_layout = QtWidgets.QVBoxLayout()
        bottom_layout = QtWidgets.QHBoxLayout()
        # check box to active the comb filter
        self.chk_FIR_comb = QtWidgets.QCheckBox("FIR Comb")
        self.chk_FIR_comb.setChecked(True)
        # whenever the state change in the checkbox call the self.change_FIRcomb function
        self.chk_FIR_comb.stateChanged.connect(self.change_FIRcomb)

        # create decimation function
        self.chk_IIR_comb = QtWidgets.QCheckBox("IIR Comb")
        self.chk_IIR_comb.setChecked(True)
        # whenever the state change in the checkbox call the self.change_IIRcomb function 
        self.chk_IIR_comb.stateChanged.connect(self.change_IIRcomb)
        check = QtWidgets.QWidget()
        check_layout.addWidget(self.chk_FIR_comb)
        check_layout.addWidget(self.chk_IIR_comb)
        check.setLayout(check_layout)
        # Create sliders
        slider_widget = QtWidgets.QWidget()        
        # self.slider_1 is for the FIR comb
        self.slider_1 = self.create_slider()
        self.slider_1.valueChanged.connect(self.redraw_FIR)
        # self.slider_2 is for the decimation
        self.slider_2 = self.create_slider()
        # whenever the state change in the checkbox call the self.redraw_down function 
        self.slider_2.valueChanged.connect(self.redraw_IIR)
        sliders_layout.addWidget(self.slider_1)
        sliders_layout.addWidget(self.slider_2)
        slider_widget.setLayout(sliders_layout)
        bottom_layout.addWidget(check)
        bottom_layout.addWidget(slider_widget)
        widget = QtWidgets.QWidget()
        widget.setLayout(bottom_layout)
        widget.setMaximumHeight(150)
        layout_vertical.addWidget(self.canva)
        layout_vertical.addWidget(widget)

        # SHOW SIGNALS
        self.fs_signal = 100
        self.h_signal = 1
        self.len_signal = 1
        self.k_max_signal = 7
        self.freq = 5
        #self.signal,self.time = self.myFourierSeries()
        #self.canva.axes1.stem(self.time,self.signal,use_line_collection=True)
        # take the fft of original signal
        #self.X_signal,self.freq_domain = self.take_fft(self.signal)
        #self.canva.axes2.stem(self.freq_domain,self.X_signal,use_line_collection=True)
        self.setCentralWidget(centralWidget)
        # upsampling and downsampling parameters
        self.createFilter(43,15,30,1000,0.001,"FIR")
        self.createFilter(43,15,30,1000,0.001,"IIR")
        self.setWindowTitle("Ahmet Cihat Bozkurt Comb Filter")
        self.showMaximized()
        self.show()
    def redraw_FIR(self):
        print("Update FIR")
    def redraw_IIR(self):
        print("Update IIR")
    def change_FIRcomb(self):
        print("BOS")

    def change_IIRcomb(self):
        print("BOS")

    def createFilter(self,numtaps,f0,f1,fs,dt,filter_type):
        if filter_type == "FIR":
            a = 1
            b = signal.firwin(numtaps,[f0,f1],fs=fs,window='hamming')
            print(b)

        else:
            b,a = signal.iirfilter(17, [50, 200], rs=60, btype='band',
                       analog=False, ftype='cheby2', fs=2000,
                       output='ba')
            print(b)



    def create_slider(self):
        # This function creates a slider and returns it.
        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider.setRange(1, 10)
        slider.setFocusPolicy(QtCore.Qt.StrongFocus)
        slider.setMinimum(1)
        slider.setTickInterval(10)
        slider.setSingleStep(1)
        return slider

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()