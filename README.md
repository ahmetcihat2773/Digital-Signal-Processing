# Digital Signal Processing Projects

This repository contains four distinct projects related to Digital Signal Processing (DSP). Each project demonstrates different DSP techniques and concepts. Below is a detailed description of each project.

## Contents

1. [Adaptive Filtering](#1-adaptive-filtering)
2. [Beamforming](#2-beamforming)
3. [Comb Filter](#3-comb-filter)
4. [Sampling](#4-sampling)

## 1. Adaptive Filtering

### Overview
The `adaptiveFiltering` project focuses on adaptive filter algorithms, which are essential for applications where the filter characteristics need to change dynamically based on the signal properties.

### Techniques Used
- **LMS (Least Mean Squares) Algorithm:** A gradient-based method used to adapt the filter coefficients to minimize the error between the desired and actual output.
- **RLS (Recursive Least Squares) Algorithm:** An advanced adaptive filtering technique that provides faster convergence and better tracking capabilities compared to LMS.

### Files
- `lms_filter.py`: Implementation of the LMS adaptive filter.
- `rls_filter.py`: Implementation of the RLS adaptive filter.
- `examples/`: Contains example scripts demonstrating the use of LMS and RLS filters on sample signals.

## 2. Beamforming

### Overview
The `beamforming` project demonstrates the principles of beamforming, a technique used in sensor arrays for directional signal reception or transmission.

### Techniques Used
- **Delay-and-Sum Beamforming:** A method that delays the signal received at each sensor to align signals from a specific direction before summing them.
- **MVDR (Minimum Variance Distortionless Response) Beamforming:** An advanced technique that optimizes the beamforming weights to minimize the output power while maintaining a distortionless response in the desired direction.

### Files
- `delay_and_sum.py`: Implementation of the delay-and-sum beamforming algorithm.
- `mvdr_beamforming.py`: Implementation of the MVDR beamforming algorithm.
- `examples/`: Contains example scripts demonstrating the use of beamforming techniques on sample data.

## 3. Comb Filter

### Overview
The `combfilter` project explores comb filters, which are used in various signal processing applications to enhance or suppress periodic components of a signal.

### Techniques Used
- **Feedforward Comb Filter:** A filter that introduces a delay in the signal and adds it to the original signal, creating a series of notches in the frequency response.
- **Feedback Comb Filter:** A filter that introduces a delay in the signal and feeds it back into the input, creating a series of peaks in the frequency response.

### Files
- `feedforward_comb.py`: Implementation of the feedforward comb filter.
- `feedback_comb.py`: Implementation of the feedback comb filter.
- `examples/`: Contains example scripts demonstrating the use of comb filters on sample signals.


## 4. Sampling

### Overview
The `Sampling` project covers the concepts of signal sampling and reconstruction, which are fundamental in digital signal processing.

### Techniques Used
- **Nyquist Sampling Theorem:** Ensures that a continuous signal can be completely represented in its samples and reconstructed if the sampling rate is greater than twice the highest frequency of the signal.
- **Aliasing:** Describes the effect when a signal is undersampled, causing different signals to become indistinguishable.

### Files
- `sampling_theorem.py`: Demonstrates the Nyquist Sampling Theorem and the effects of aliasing.
- `examples/`: Contains example scripts for sampling and reconstruction of signals.
