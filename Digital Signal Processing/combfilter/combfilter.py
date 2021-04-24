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
        fs = 8000
        fs2 = 8000/2
        f1 = 500
        f2 = 2500
        numtaps = 43
        dt = 1/fs
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

        #self.canva.axes1.stem(self.time,self.signal,use_line_collection=True)
        #self.canva.axes2.stem(self.freq_domain,self.X_signal,use_line_collection=True)
        self.setCentralWidget(centralWidget)


        self.createFilter(numtaps,f1,f2,fs,dt,"FIR")
        self.createFilter(numtaps,f1,f2,fs,dt,"IIR")

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

    def createFilter(self,numtaps,f1,f2,fs,dt,filter_type):
        """
        This function creates filters and returns a and b coefficients and frequency and amplitude.
        """

        # numtaps : length of a filter. Number of coefficients.(filter order + 1)
        if filter_type == "FIR":
            # fir filter's a coefficient is 1.
            a = 1
            b = signal.firwin(numtaps,[f1,f2],fs=fs,window='hamming',pass_zero='bandpass')
            freq, amp = signal.freqz(b,a,fs=fs)
            # get b coefficient thanks to firwin function.
            amp = 20*np.log10(abs(amp)) 
            self.canva.axes1.plot(freq,amp)
            return a,b
        else:
            b,a = signal.iirfilter(numtaps, [f1,f2],btype='bandpass',
                       analog=False, ftype='cheby1',rp=3,rs=20,fs=fs,
                       output='ba')
            freq, amp = signal.freqz(b,a,fs=fs)
            amp = 20*np.log10(abs(amp)) 
            self.canva.axes3.plot(freq,amp)
            return a,b

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