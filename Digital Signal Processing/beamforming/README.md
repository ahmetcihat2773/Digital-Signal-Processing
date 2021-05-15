# Acoustics I - Noise Source Location
Acoustic beamforming is a technique to measure the sound pressure thanks to some microphones arrays and also that is able to locate the sound source, either meaningful or noise by processing the collected sound signals. This technique involved in many academic and industrial applications. 

In daily life, noise sound is one of the main problems of today's world. Every produced vehicle, machine, or tool has to have a sound noise below some certain level according to some standards [13]. Detecting the noise source in a device is a challenging task for engineers. However, using beam forming is one of the most successful noise localization techniques that allows engineers to distinguish each and individual noise sources [14].

Thanks to all development in technology, we are able to build robust microphone arrays that are equipped with more than a hundred microphones which allows us to perform precise noise source localization [13]. One can face the noise source localization problem in automotive, telecommunication, aerospace industry, etc. Noise source localization of airfoil will be explained here as an example.  

Nowadays, environmental issue is one of the most dominant problems in the air transportation system. Airplanes should make as little noise as possible during landing and taking off. Understanding which part causes noise in airplanes requires long-term research and technical infrastructure on its own. Although there are many methods, the beam forming method will be explained.

In the photo below, a scaled aircraft is used to investigate the noise which is caused on the wings by the wind turbine air. In order to find the exact location of the noise, microphone arrays are placed on the ground and the calculated noise powers can be seen in the right of the below image.   

<img align="center" src="images/airfoil.PNG">

<sub>Image Source: [13] </sub>

In another application of airfoil noise localization which is performed in the University of Twente Aeroacoustic Wind Tunnel, the set-up with 112 digital MEMS microphones and FPGA is used for noise source measurement which is given in the image below.


<img align="center" src="images/mic.PNG"  >
<sub>Image Source: [13] </sub>

In this application, the wind is coming from left to right and the placement of the microphones or sensors is optimized to improve the array performance. That's why the placement of the arrays also affects the result of beam forming. 


Delay and Sum technique is already explained before. The area where the noise source is likely to be is divided into grids. Each point of these grids is considered as a noise source and the source pressure levels ​​are obtained by applying the delay-and-sum technique to the signals coming from the points. These values can be presented on a counter map [15].

<img align="center" src="images/beamforming.PNG"  >
<sub>Image Source: [13] </sub>

In the given image above, $m$ represents the microphones, $x$ represents the possible noise source in an area and all the signals are captured by the microphones. Output Map is given for only one location which can be calculated with the given formula below [13]. 


\[L(t,t_{0}) = \frac{4\Pi}{M} \sum_{m=1}^{M}p_{m}(x_{0},t+t_{0})|x-x_{0}|\]

Here $M$ is the total number of microphones, $p_{m}$ is the signal measured by each microphone, $x_{1}$ is the one possible source position, $x$ is the microphone position. 

Here the $t_{0}$ is important because it represents the delay and intentionally added to the equation. For each node or possible source location, the signal measured by each microphone is delayed according to the behinded time with the given formula below.

\[t_{0} = \frac{x-x_{0}}{c_{0}} \]



# Beamforming in Radar
Radars are electromagnetic sensors that are used for the range, angle, or velocity determination of objects. They can be used for detecting motor vehicles, spacecraft, cars, etc. There might be one or more than one transmitter and receiver antennas in radar to detect the mentioned properties of any object. In principle, radars send signals from transmitters and the signals they send come back by hitting an object. The returning signals are picked up by the receivers.
The distance of an object in the coverage area of ​​the radar is calculated by the time it takes the signal to leave and return to the radar. There is a lot of different application of radar in industry and academy [16] however I am going to explain the digital beam forming radars. Besides getting velocity, digital beam-forming radars provide distance and angular information of possible target objects. In general, a good angular resolution which means a large field of view is required for many applications [17]. In order to achieve this high resolution, the number of receivers and transmitters should be increased. For example, eight transmitters and eight receivers on radar can be one option and multiple transceiver and transmitter configuration can be seen in the image below [17].

<img align="center" src="images/radarSensor.PNG" >

<sub>Image Source: [17] </sub>

In one of the applicaiton, two stationary objects are aimed to be detected by the radar. In order to detect them, radar has to calculate the distance of the object by considering the time delay during the propagation and has to calculate the angle where the object is located by considering the frequency domain of the signal. To do this, FFT is used in the receiver part because of the frequency modulation characteristic [17]. Frequency modulated signals have high frequency where the source signal has high amplitude and low frequency where the source signal has low amplitude. 

<img align="center" src="images/fmcw.gif"  >

<sub>Image Source: https://en.wikipedia.org/wiki/Frequency_modulation  </sub>


After getting the angle and distance the location of the objects can be obtained. 
On the left side of the figure below, two corner reflectors are placed with different distances and height in front of the radar. Each corner reflectors have different cross sections. In the radar, frequency-modulated continuous waves are used and the image on the right side of the given image below is obtained after applying the beam forming in which one can see where the relative power is increasing which represents the object in $x,y$. The radar is located at 0,0 and the right side is positive in x coordinate and the left side of the radar is negative.

<img align="center" src="images/ImagingResults.PNG"  >
<sub>Image Source: [20] </sub>

# Beamforming In Sonar Applications
Sonar means Sound Navigation and Ranging which is useful for exploring and mapping the oceans by using sound waves. Since the sound speed is constant, it can be used for calculating the distance from Sonar itself. The distance of an object is calculated by measuring the time that takes the sound waves return after having transmitted from the transmitter. Therefore reflected sound signals are used. When the transmitter emitting time and the time that the receiver has the reflected sound signal is known, the distance can be calculated easily.

<img align="center" src="images/sonarReflector.PNG"  >

<sub>Image Source: [19] </sub>

Beamforming is used for detecting fish population density under the water. 

<img align="center" src="images/fish.PNG"  >

<sub>Image Source: [19] </sub>

Sonar is used for 2D or 3D mapping of the seafloor by estimating range in different levels with beam forming methods.

<img align="center" src="images/seafloor.PNG"  >

<sub>Image Source: [19] </sub>

Detection of the object in the seafloor is of growing in importance right now in the current underwater research. Thanks to these researches mines, toxic wastes, or archeological findings can be found which are vitally important for people and nature [18].


# References : 

13. Department Thermal Fluid Engineering University of Twente (n.d.) Fundamentals of Acoustic Beamforming, P.O. Box 217 Enschede, 7500 AE The Netherlands: Leandro de Santana.
14. National Instruments (n.d.) Using Acoustic Beamforming for Pass-By Noise Source Detection, P.O. Box 217 Enschede, 7500 AE The Netherlands: Doug Farrell,Product Manager.
15. (2003) Noise Source Location Techniques – Simple to Advanced Applications, P.O. Box 217 Enschede, 7500 AE The Netherlands: Mehdi Batel and Marc Marroquin, Brüel & Kjær North America, Inc., Norcross, Georgia Jørgen Hald, Jacob J. Christensen, Andreas P. Schuhmacher and Torben G. Nielsen, Brüel & Kjær, Denmark.
16. (20 January 2021) Radar configurations and Types, Available at: https://en.wikipedia.org/wiki/Radar_configurations_and_types
17. Marlene Harter, Andreas Kornbichler, Thomas Zwick (2010) A Modular 24 GHz Radar Sensor for Digital Beamforming on Transmit and Receive
18. (2006) Acoustic Imaging of Underwater Embedded Objects: Signal Simulation for Three-Dimensional Sonar Instrumentation, : Maria Palmese, Member, IEEE, and Andrea Trucco, Senior Member, IEEE.
19. Department of Informatics, University of Oslo (September 2013) Introduction to Sonar INF-GEO4310, : Roy Edgar Hansen.
20. (October 2011) Three-dimensional radar imaging by digital beamforming, : Marlene Harter,Andreas Ziroff,Thomas Zwick.