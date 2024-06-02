# Calculation of UHII / Analysis of the relationship between the UHII and Pollutant Density in Kanto Region

This is a programme produced as part of ALESS (Active Learning of English for Science Students), a class for first-year undergraduates at the University of Tokyo to learn to write papers in English.  
It uses temperature [data from the Japan Meteorological Agency (JMA)](https://www.data.jma.go.jp/stats/etrn/index.php?prec_no=&block_no=&year=&month=&day=&view=) 
and data from the National Institute for Environmental Studies' 
“[Environmental Observatory: Air Pollution Continuous Monitoring Data](https://tenbou.nies.go.jp/download/)” and 
“[Atmospheric Environment Measurement Station Data](https://www.nies.go.jp/igreen/tm_down.html)”. (retrieved on 2 Jun 2024)

The code here is for viewing only and is not intended for re-use, but if you wish to use it, please follow these steps.
1. Download/install Python, the required packages and Google Chrome.
2. Download/process the National Institute for Environmental Studies data as described in asys.py.
3. Replace the email address in temptest.py line 24 with your own.
4. Execute asys.py, calc_epd.py and correlation.py in this order.
Note that all the files necessary for analysis are available at the point of running calc.epd.py, so it is possible to try different analysis methods with different files from correlation.py.

The files are as follows.  
asys.py: file for collecting data and calculating UHII.  
calc_epd.py: file for interpolating pollutant data and calculating concentrations at locations corresponding to temperature stations.  
constants.py: file defining the data retention classes.  
coord.json: file in which the data for the locations used in the experiment were collected from the JMA data page mentioned above and rewritten in a usable form.  
correlation.py: file for calculating correlation coefficients and plotting graphs.  
readme-en.md: English translation of readme.md.  
readme.md: repository description file.  
temptest.py: file for scraping average temperatures from the JMA website.

Tested on Python 3.12.2, MacBook Pro (with M3 chip, 12-core CPU, and 36GB memory)  
Google Chrome's version was 125.0.6422.141 (Official Build) (arm64)

Python Libraries which were directly used:  
beautifulsoup4 (https://pypi.org/project/beautifulsoup4/) v4.12.3  
chromedriver-binary (https://github.com/danielkaiser/python-chromedriver-binary) v125.0.6422.78.0  
dill (https://github.com/uqfoundation/dill) v0.3.8  
geographiclib (https://geographiclib.sourceforge.io/Python/2.0) v2.0  
matplotlib (https://pypi.org/project/matplotlib/) v3.9.0  
numpy (https://numpy.org) v1.26.4  
selenium (https://www.selenium.dev) v4.21.0