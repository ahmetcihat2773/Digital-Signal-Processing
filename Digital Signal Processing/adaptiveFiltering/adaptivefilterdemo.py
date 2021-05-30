# Aim : Realizing the one of possible scenario in microphnes. There are two microphones and one get signal later due
# to propagation. Purpose of  this program calculating this delay by using cross correlation and removing the noise
# from the delayed signal by using adaptive filter.
# Features : Learning rate of the adaptive filter can be changed thanks to scroll bar and the affact can be observed.
# Sampling frequency can be changed which affect the delay and the results can be observed. 
# Course : Digital Signal Processing 2, Salzburg Universty of Applied Science
# Author : Ahmet Cihat Bozkurt

import sys
import matplotlib
from matplotlib.pyplot import legend
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
from scipy import signal
from myadaptivefilt import my_lms_filter,my_fast_conv
import padasip as pa


class SignalPlotting(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # Create subplots to show the signals
        self.fig = Figure(figsize=(width, height), dpi=dpi,tight_layout=True)
        
        self.axes1 = self.fig.add_subplot(2,2,1)
        self.axes1.set_title("Signals at MIC1 and MIC2")
        self.axes1.set_xlabel("Time(s)")
        self.axes1.set_ylabel("Amplitude(V)")
        self.axes2 = self.fig.add_subplot(2,2,2)
        self.axes2.set_title("Signals at MIC1 and MIC2 After Removing Delay")
        self.axes2.set_xlabel("Time(s)")
        self.axes2.set_ylabel("Amplitude(V)")
        self.axes3 = self.fig.add_subplot(2,2,3)
        self.axes3.set_title("Signal at MIC2 Before and After Adaptive Filter")
        self.axes3.set_xlabel("Time(s)")
        self.axes3.set_ylabel("Amplitude(V)")
        self.axes4 = self.fig.add_subplot(2,2,4)
        self.axes4.set_title("Error")
        #self.axes4.set_xlabel("")
        #self.axes4.set_ylabel("")
        # Define Constant variables.

        super(SignalPlotting, self).__init__(self.fig)
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # Create an instance of the SignalPlotting class
        self.canva = SignalPlotting(self, width=5, height=4, dpi=100)
        toolbar =  NavigationToolbar(self.canva,self.canva)
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
        self.chk_FIR_comb = QtWidgets.QCheckBox("Learning Rate(Mu)")
        self.chk_FIR_comb.setChecked(True)
        self.FIR_label = QtWidgets.QLabel("   Mu : 0.01")
        hor_check1.addWidget(self.chk_FIR_comb)
        hor_check1.addWidget(self.FIR_label)
        # whenever the state change in the checkbox call the self.change_FIRcomb function
        self.chk_FIR_comb.stateChanged.connect(self.FIRcomb_check)

        # create decimation function
        self.chk_IIR_comb = QtWidgets.QCheckBox("Sampling Frequency")
        self.chk_IIR_comb.setChecked(True)
        self.IIR_label = QtWidgets.QLabel(" Fs(Hz) : 1000")
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
        self.slider_1 = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_1.setRange(1, 10)
        self.slider_1.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.slider_1.setMinimum(1)
        self.slider_1.setTickInterval(10)
        self.slider_1.setSingleStep(1)
        self.slider_1.valueChanged.connect(self.update_FIR_factor)
        # self.slider_2 is for the IIR comb
        self.slider_2 = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_2.setRange(1, 10)
        self.slider_2.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.slider_2.setMinimum(1)
        self.slider_2.setTickInterval(10)
        self.slider_2.setSingleStep(1)
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
        self.fs = 1000
        self.mu = 0.01
        self.update_after_fs()
        self.setCentralWidget(centralWidget)
        self.setWindowTitle("Ahmet Cihat Bozkurt Adaptive Filter")
        self.showMaximized()
        self.show()
    def update_FIR_factor(self):
        # Apply adaptive Filter again            
        factor = self.slider_1.value()/1000 
        label = "  Mu : " +str(factor)
        self.FIR_label.setText(label)
        self.mu = factor
        # get factor from slider
        self.update_after_fs()

    def update_IIR_factor(self):
        # Update sampling frequency
        factor = 1000*self.slider_2.value() 
        label = "  FS :  " +str(factor)
        self.IIR_label.setText(label)
        self.fs = factor
        self.update_after_fs()

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

    def update_after_fs(self):
        distance = 1 # m
        sound_speed = 343 # m/s
        self.delay_second = distance/sound_speed
        self.delay_sample = int(self.delay_second * self.fs)        
        t= np.arange(0, 1, 1/self.fs) 
        # Generate low pass filter
        b, a = signal.butter(3, 0.05)
        # Apply low pass filter to random signal
        self.source_signal = 10*signal.filtfilt(b, a, np.random.randn(len(t)))
        # Create bigger zeros signal to have a delay feeling.
        self.channel_noise = np.random.randn(len(self.source_signal)+self.delay_sample)
        # Create noise. Noise should have low power.
        b = [1, -0.8, 0.4, -0.2]
        self.channel_noise = 0.1*signal.filtfilt(b, 1, self.channel_noise)
        self.channel_noise_mic1 = np.zeros(len(self.channel_noise))
        self.channel_noise_mic1[0:len(self.source_signal)] = self.source_signal
        self.channel_noise_mic1[len(self.source_signal)::] = self.channel_noise[len(self.source_signal)::]
        self.t_channel = np.linspace(0, 1+self.delay_second, len(self.channel_noise_mic1))
        # Here mic1 has all channel with noise and source signal.

        # CREATE SIGNAL AT MIC2 
        # channel noise will be the same.
        self.channel_noise_mic2 = np.zeros(len(self.channel_noise))
        self.channel_noise_mic2[0:self.delay_sample] = self.channel_noise[0:self.delay_sample] 
        self.channel_noise_mic2[self.delay_sample::] = self.channel_noise[self.delay_sample::] + self.source_signal
        # Here the source signal is shifted to right in time by delay sample which is calculated 
        # with the distance and speed
        self.canva.axes1.clear()
        self.canva.axes1.plot(self.t_channel,self.channel_noise_mic2,'b',label="Signal at MIC2")
        self.canva.axes1.plot(self.t_channel,self.channel_noise_mic1,'r',label="Signal at MIC1")
        self.canva.axes1.legend()
        self.canva.axes1.set_title("Signals at MIC1 and MIC2")
        self.canva.axes1.set_xlabel("Time(s)")
        self.canva.axes1.set_ylabel("Amplitude(V)")
        self.canva.draw()
        
        
        # Allign the signals.
        
        self.channel_noise_mic2_flip = np.flip(self.channel_noise_mic2)  
        R = my_fast_conv(self.channel_noise_mic1,self.channel_noise_mic2_flip)
        t_cross = np.linspace(-len(self.channel_noise_mic1),len(self.channel_noise_mic1),len(R))
        # Find the delay by finding the maximum in cross correlation.
        self.delayed_samples = np.where(R ==max(R))[0]
        self.delayed_sample = len(self.channel_noise_mic2_flip) - self.delayed_samples 
        self.delayed_sample = list(self.delayed_sample)[0] - 1 
        self.channel_noise_mic2[0:len(self.channel_noise_mic2)-self.delayed_sample] = self.channel_noise_mic2[self.delayed_sample::]
        self.channel_noise_mic2[len(self.channel_noise_mic2)-self.delayed_sample::] = self.channel_noise[(len(self.channel_noise_mic2)-self.delayed_sample)::]
        
        self.canva.axes2.clear()
        self.canva.axes2.plot(self.t_channel,self.channel_noise_mic2,'b',label="Signal at MIC2")
        self.canva.axes2.plot(self.t_channel,self.channel_noise_mic1,'r',label="Signal at MIC1")
        self.canva.axes2.legend()
        self.canva.axes2.set_title("Signals at MIC1 and MIC2 After Removing Delay")
        self.canva.axes2.set_xlabel("Time(s)")
        self.canva.axes2.set_ylabel("Amplitude(V)")
        self.canva.draw()
        
        filter_order = 5
        self.input_matrix = pa.input_from_history(self.channel_noise_mic1, filter_order)[:-1]
        self.channel_noise_mic2_temp = self.channel_noise_mic2[0:len(self.channel_noise_mic2)-filter_order]
        b_init = np.random.rand(len(self.channel_noise_mic1),filter_order)
        self.y, self.e, w = my_lms_filter(self.channel_noise_mic2_temp,self.input_matrix,self.mu,b_init)
        #f = pa.filters.FilterLMS(n=filter_order, mu=self.mu, w="random")
        #self.y, self.e, w = f.run(self.channel_noise_mic2_temp,self.input_matrix)
        self.t_channel = np.linspace(0, 1+self.delay_second, len(self.channel_noise_mic2_temp))
        self.canva.axes3.clear()
        self.canva.axes3.plot(self.t_channel,self.channel_noise_mic2_temp,'b',label="Before Adaptive Filter")
        self.canva.axes3.plot(self.t_channel,self.y,'r',label="After Adaptive Filter")
        self.canva.axes3.legend()
        self.canva.axes3.set_title("Signal at MIC2 Before and After Adaptive Filter")
        self.canva.axes3.set_xlabel("Time(s)")
        self.canva.axes3.set_ylabel("Amplitude(V)")

        self.canva.draw()
        self.canva.axes4.clear()
        self.canva.axes4.plot(10*np.log10(self.e**2),'b',label="e - error [dB]")
        self.canva.axes4.set_xlabel("Sample")
        self.canva.axes4.set_ylabel("dB")
        self.canva.axes4.legend()
        self.canva.axes4.set_title("Error")
        self.canva.draw()
        


        
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()