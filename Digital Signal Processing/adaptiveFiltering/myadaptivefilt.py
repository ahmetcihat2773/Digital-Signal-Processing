import numpy as np
def my_lms_filter(d,x,mu,b):
    """
    d is source signal without any noise. shape (n,1)
    input_matrix = x,  this is the source signal + noise :: shape(n,5)
    """
    k = 0
    y = list()
    e = list()
    for samples in x:
        y.append(np.dot(b[k],samples))      
        e.append(d[k] - y[k])
        b[k+1] = b[k] + mu*e[k]*samples
        k = k + 1 
    return y, np.array(e), b

def my_fast_conv(x, h):
  # Converting into frequency domain and multiplying and returning time domain 1000 times faster.
  # transform the x and h into frequency domain and multiply them and then come back to time domain
    # YOUR CODE HERE
    fftsize_x = len(x)
    fftsize_h = len(h)
    fftsize = fftsize_x + fftsize_h -1 

    X = np.fft.fft(x,fftsize)
    H = np.fft.fft(h,fftsize)
    Y = X * H
    # Inverse fourier transform
    y = np.fft.ifft(Y,fftsize)
    
    return abs(y)