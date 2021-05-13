# Beamforming
In communication, beamforming is used to increase the quality of communication. On the other hand, beam forming also can be used to detect the direction of source signal.
The beamforming, i.e., spatial filtering, aims to suppress signals arriving from undesirable directions while amplifying signals from desired directions.

Beamforming is used deliver sufficient gain and sensitivity for radio observations while maintaining
control over beam pattern sidelobes and system noise.8
# Acoustics I - Noise Source Location
Acoustic beamforming is a technique to measure the sound pressure thanks to some microphones arrays and also that is able to locate the sound source, either meaningfull or noise by processing the collected sound signals. This technique involved in many acedemic and industrial applications. In daily life, sound noise is one of the main problem of the today world. Every produced vehicle, machines or any tools have to have a sound noise below some certain level according to some standarts[]. Detecting the noise source in a device is a challenging task for engineers. However beamforming is one of the most successful noise localization technique that allows engineers to distinguish each and individual noise sources[].
Thanks to all development in technologhy, we are able to build robust microphone arrays that is equipped with more than a hundred of microphones which allows us to perform preciese noise source localization[Fundamentals of Acustic BeamformingXX.pdf]. One can face with the noise source localization problem in automative, telecommunication, aerospace industrt etc. Noise source localization of airfoil will be explained here as an example. 

Nowadays, enviromental issue is one of the most dominant problem in air transportation system. Airplanes should make as little noise as possible during landing and taking off.Understanding which part causes noise in airplanes requires a long-term research and technical infrastructure on its own. Although there are many different methods, the beamforming method will be explained.

In the photo below, a scaled aircraft is used to investigate the noise which is caused on the wings by the wind tirbune air. In order to find the exact location of the noise, microphone arrays are placed on the ground and the calculated noise powers can be seen in the right of the below image.  
![airfoil](airfoil.PNG)

In another application of airfoil noise localization which is performed in the University of Twente Aeroacoustic Wind Tunnel, the set-up with 112 digital MEMS microphone and FPGA is used to noise source measurement which is given in the image below. 

![airfoil](mic.PNG)

In this application the wind is coming from left to right and the placement of the microphones or sensors are optimized to improve the array performance. That's why the placement of the arrays also affect the result of beamforming. 


Delay and Sum technique is aldready explained before. The area where the noise source is likely to be is divided into grids. Each point of these grids is considered as a noise source and the power values ​​are obtained by applying the delay-and-sum technique for the signals coming from the points.


![airfoil](beamforming.PNG)

In the given image above, m represents the microphones, x represents the possible noise source in an area and all the signals are captured by the microphones. Output Map is given for only one location which can be calculated with the given formula below. [Fundamentals of aerospace etc] 


<img align="center" src="http://www.sciweavers.org/upload/Tex2Img_1620886835/render.png">


Here M is the total number of microphones, pm is the signal measured by each microphone, x1 is the one possible source position, x is the microphone position. 

Here the t0 is important because, it represents the delay and intentionally added to the equaiton. For each node or possible source location, signal measured by the each microphone is delayed according to the behinded time with the given formula below.


<img align="center" src="http://www.sciweavers.org/upload/Tex2Img_1620887945/render.png">


