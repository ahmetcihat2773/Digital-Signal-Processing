import sys
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
from scipy import signal
from combfilter import combfilter
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
        self.fs = 8000
        f1 = 500
        f2 = 2500
        numtaps = 43
        dt = 1/self.fs
        self.FIRchecked  = True
        self.IIRchecked = True
        # Create an instance of the SignalPlotting class
        self.canva = SignalPlotting(self, width=5, height=4, dpi=100)
        # create a flexible layout
        centralWidget = QtWidgets.QWidget()
        layout_vertical = QtWidgets.QVBoxLayout()
        centralWidget.setLayout(layout_vertical)
        check_layout = QtWidgets.QVBoxLayout()
        sliders_layout = QtWidgets.QVBoxLayout()
        hor_check1 = QtWidgets.QHBoxLayout()
        widget_check1 = QtWidgets.QWidget()
        widget_check1.setLayout(hor_check1)

        hor_check2 = QtWidgets.QHBoxLayout()
        widget_check2 = QtWidgets.QWidget()
        widget_check2.setLayout(hor_check2)



        bottom_layout = QtWidgets.QHBoxLayout()
        # check box to active the comb filter
        self.chk_FIR_comb = QtWidgets.QCheckBox("FIR Comb")
        self.chk_FIR_comb.setChecked(True)
        self.FIR_label = QtWidgets.QLabel("  Factor:  1")
        hor_check1.addWidget(self.chk_FIR_comb)
        hor_check1.addWidget(self.FIR_label)
        # whenever the state change in the checkbox call the self.change_FIRcomb function
        self.chk_FIR_comb.stateChanged.connect(self.FIRcomb_check)

        # create decimation function
        self.chk_IIR_comb = QtWidgets.QCheckBox("IIR Comb")
        self.chk_IIR_comb.setChecked(True)
        self.IIR_label = QtWidgets.QLabel("  Factor:  1")
        hor_check2.addWidget(self.chk_IIR_comb)
        hor_check2.addWidget(self.IIR_label)
        # whenever the state change in the checkbox call the self.change_IIRcomb function 
        self.chk_IIR_comb.stateChanged.connect(self.IIRcomb_check)
        check = QtWidgets.QWidget()
        check_layout.addWidget(widget_check1)
        check_layout.addWidget(widget_check2)
        check.setLayout(check_layout)
        # Create sliders
        slider_widget = QtWidgets.QWidget()        
        # self.slider_1 is for the FIR comb
        self.slider_1 = self.create_slider()
        self.slider_1.valueChanged.connect(self.update_FIR_factor)
        # self.slider_2 is for the IIR comb
        self.slider_2 = self.create_slider()
        # whenever the state change in the checkbox call the self.redraw_down function 
        self.slider_2.valueChanged.connect(self.update_IIR_factor)
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


        self.FIR_a,self.FIR_b = self.createFilter(numtaps,f1,f2,dt,"FIR")
        self.IIR_a,self.IIR_b  = self.createFilter(numtaps,f1,f2,dt,"IIR")

        self.setWindowTitle("Ahmet Cihat Bozkurt Comb Filter")
        self.showMaximized()
        self.show()
    def update_FIR_factor(self):
            
            factor = self.slider_1.value() 
            label = "  Factor:  " +str(factor)
            self.FIR_label.setText(label)
            # get factor from slider
            b,a = combfilter(self.FIR_b,self.FIR_a, factor)
            # get combfilter coefficients
            freq, amp = signal.freqz(b,a,fs=self.fs)
            amp = 20*np.log10(abs(amp)) 
            self.canva.axes2.clear()
            self.canva.axes2.plot(freq,amp)
            self.canva.draw()

    def update_IIR_factor(self):

            factor = self.slider_2.value() 
            label = "  Factor:  " +str(factor)
            self.IIR_label.setText(label)
            # get factor from slider
            b,a = combfilter(self.IIR_b,self.IIR_a, factor)
            # get combfilter coefficients
            freq, amp = signal.freqz(b,a,fs=self.fs)
            amp = 20*np.log10(abs(amp)) 
            self.canva.axes4.clear()
            self.canva.axes4.plot(freq,amp)
            self.canva.draw()

    def FIRcomb_check(self,state):

        if state == QtCore.Qt.Checked:
        
            self.slider_1.setDisabled(False)

        else:
        
            self.slider_1.setDisabled(True)    
            
    def IIRcomb_check(self,state):

        if state == QtCore.Qt.Checked:

            self.slider_2.setDisabled(False) 
        
        else:
        
            self.slider_2.setDisabled(True) 

        
    def createFilter(self,numtaps,f1,f2,dt,filter_type):
        """
        This function creates filters and returns a and b coefficients and frequency and amplitude.
        """

        # numtaps : length of a filter. Number of coefficients.(filter order + 1)
        if filter_type == "FIR":
            # fir filter's a coefficient is 1.
            a = 1
            b = signal.firwin(numtaps,[f1,f2],fs=self.fs,window='hamming',pass_zero='bandpass')
            freq, amp = signal.freqz(b,a,fs=self.fs)
            # get b coefficient thanks to firwin function.
            amp = 20*np.log10(abs(amp)) 
            self.canva.axes1.plot(freq,amp)
            return a,b
        else:
            b,a = signal.iirfilter(numtaps, [f1,f2],btype='bandpass',
                       analog=False, ftype='cheby1',rp=3,rs=20,fs=self.fs,
                       output='ba')
            freq, amp = signal.freqz(b,a,fs=self.fs)
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