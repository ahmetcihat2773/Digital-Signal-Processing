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
        self.axes1 = self.fig.add_subplot(3,2,1)
        self.axes1.set_title("Original Square Wave")
        self.axes1.set_xlabel("Time(seconds)")
        self.axes1.set_ylabel("x(t)")
        self.axes2 = self.fig.add_subplot(3,2,2)
        self.axes2.set_title("Original Linear Spectrum")
        self.axes2.set_xlabel("Frequency(Hz)")
        self.axes2.set_ylabel("X(f)")
        self.axes3 = self.fig.add_subplot(3,2,3)
        self.axes3.set_title("Upsampled Square Wave")
        self.axes3.set_xlabel("Time(seconds)")
        self.axes4 = self.fig.add_subplot(3,2,4)
        self.axes4.set_title("Upsampled Linear Spectrum")
        self.axes4.set_xlabel("Frequency(Hz)")
        self.axes5 = self.fig.add_subplot(3,2,5)
        self.axes5.set_title("Downsampled Square Wave")
        self.axes5.set_xlabel("Time(seconds)")
        self.axes6 = self.fig.add_subplot(3,2,6)
        self.axes6.set_title("Downsampled Linear Spectrum")
        self.axes6.set_xlabel("Frequency(Hz)")
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
        # check box to active the interpolation
        self.chk_interpolation = QtWidgets.QCheckBox("Interpolation")
        self.chk_interpolation.setChecked(True)
        # whenever the state change in the checkbox call the self.change_upsample function
        self.chk_interpolation.stateChanged.connect(self.change_upsample)

        # create decimation function
        self.chk_decimation = QtWidgets.QCheckBox("Decimation")
        self.chk_decimation.setChecked(True)
        # whenever the state change in the checkbox call the self.change_downsample function 
        self.chk_decimation.stateChanged.connect(self.change_downsample)
        check = QtWidgets.QWidget()
        check_layout.addWidget(self.chk_interpolation)
        check_layout.addWidget(self.chk_decimation)
        check.setLayout(check_layout)
        # Create sliders
        slider_widget = QtWidgets.QWidget()        
        # self.slider_1 is for the interpolation
        self.slider_1 = self.create_slider()
        self.slider_1.valueChanged.connect(self.redraw_up)
        # self.slider_2 is for the decimation
        self.slider_2 = self.create_slider()
        # whenever the state change in the checkbox call the self.redraw_down function 
        self.slider_2.valueChanged.connect(self.redraw_down)
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
        self.signal,self.time = self.myFourierSeries()
        self.canva.axes1.stem(self.time,self.signal,use_line_collection=True)
        # take the fft of original signal
        self.X_signal,self.freq_domain = self.take_fft(self.signal)
        self.canva.axes2.stem(self.freq_domain,self.X_signal,use_line_collection=True)
        self.setCentralWidget(centralWidget)
        # upsampling and downsampling parameters
        self.up_coef = 1
        self.down_coef = 1
        # APPLY UPSAMPLE
        self.upsampled()
        # APPLY DOWNSAMPLE
        self.downsampled()
        self.setWindowTitle("Ahmet Cihat Bozkurt LAB3")
        self.showMaximized()
        self.show()
    def redraw_up(self):
        # Whenever the slider position change apply the upsampling again and show the result.
        self.up_coef = self.slider_1.value()
        self.upsampled()
    def redraw_down(self):
        # Whenever the slider position change apply the downsampling again and show the result.
        self.down_coef = self.slider_2.value()
        self.downsampled()

    def change_upsample(self):
        # Whenever the check boxes state change, enable or disable the slider.
        if self.chk_interpolation.isChecked() == True:
            self.slider_1.setEnabled(True)
        else:
            self.slider_1.setDisabled(True)
    def change_downsample(self):
        # Whenever the check boxes state change, enable or disable the slider.
        if self.chk_decimation.isChecked() == True:
            self.slider_2.setEnabled(True)
        else:
            self.slider_2.setDisabled(True)

    def upsampled(self):
        # Create the new upsampled signal with zeros
        self.up_signal = np.zeros(self.fs_signal*(self.up_coef))
        # Take each sample from self.signal and add them to the self.up_coef'th sample 
        self.up_signal[::self.up_coef] = self.signal 
        # Create the FIR filter since I am doing the interpolation in time domain.
        numtaps = 30 # This is number of coefficient
        f_cutoff = 0.1 # We need the low frequency components.
        FIR_filter = signal.firwin(numtaps=numtaps,cutoff=f_cutoff)
        # apply the filer
        self.up_signal = signal.lfilter(b=FIR_filter,a=[1],x=self.up_signal)
        self.t_up = np.linspace(0,self.len_signal,len(self.up_signal))  
        # take the fft to show the result
        self._X,freq = self.take_fft(self.up_signal)
        self.canva.axes3.clear()
        self.canva.axes3.stem(self.t_up,self.up_signal,use_line_collection=True) 
        self.canva.axes3.set_title("Upsampled Square Wave Factor "+str(self.up_coef))
        self.canva.axes3.set_xlabel("Time(seconds)")
        self.canva.axes3.set_ylabel("x(t)")
        self.canva.axes4.clear()
        self.canva.axes4.stem(freq,self._X,use_line_collection=True)
        self.canva.axes4.set_title("Upsampled Linear Spectrum with Factor "+str(self.up_coef))
        self.canva.axes4.set_xlabel("Frequency(Hz)")
        self.canva.axes4.set_ylabel("X(f)")
        self.canva.fig.canvas.draw()
    def downsampled(self):
        # create the downsampled signal with zeros.
        self.down_sampled = np.linspace(0, self.len_signal,int(np.ceil(self.fs_signal /self.down_coef)))
        self.down_sampled = self.signal[::self.down_coef]
        self.t_down = np.linspace(0,self.len_signal,len(self.down_sampled))
        # SHOW FREQUENCY DOWNSAMPLED
        X_up,freq = self.take_fft(self.down_sampled)
        self.canva.axes5.clear()
        self.canva.axes5.stem(self.t_down,self.down_sampled,use_line_collection=True)
        self.canva.axes5.set_title("Downsampled Square Wave Factor "+str(self.down_coef))
        self.canva.axes5.set_xlabel("Time(seconds)")
        self.canva.axes5.set_ylabel("x(t)")
        self.canva.axes6.clear()
        self.canva.axes6.stem(freq,X_up,use_line_collection=True)
        self.canva.axes6.set_title("Downsampled Linear Spectrum with Factor "+str(self.down_coef))
        self.canva.axes6.set_xlabel("Frequency(Hz)")
        self.canva.axes6.set_ylabel("X(f)")
        self.canva.fig.canvas.draw()
    def take_fft(self,signal):
        # This function takes the fft and returns the frequency domain and frequency components.
        X = np.fft.fft(signal)
        X = np.abs(X)
        freq = np.fft.fftfreq(len(X),1/self.fs_signal)
        return X,freq

    def create_slider(self):
        # This function creates a slider and returns it.
        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider.setRange(1, 10)
        slider.setFocusPolicy(QtCore.Qt.StrongFocus)
        slider.setMinimum(1)
        slider.setTickInterval(10)
        slider.setSingleStep(1)
        return slider
    def myFourierSeries(self):
        """
        This function creates square wave from fourier series. 
        """
        
        # k_max_signal :  maximum of order of the fourier series. [1 21]
        # h_signal : Square wave amplitude
        # fs_signal : signal sampling frequency.
        # len_signal : length of the signal in second.
        
        t = np.arange(0,self.len_signal,1/self.fs_signal)
        f = 0
        for i in range(1,self.k_max_signal+2,2):
            # here I applied the formula which is given above.     
            f = f + (1/i)*np.sin(2*self.freq*np.pi*i*t)
        f = f*(4*self.h_signal/np.pi)
        # f is the fourier series, formula above is applied.
        return f,t
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()