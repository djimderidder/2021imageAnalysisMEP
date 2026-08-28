Image analysis code from my MSc thesis (Koenderink Lab, TU Delft, 2021–2022), studying septin in the actin cortex.
For this, we reconstituted the filament network on model membranes and imaged with atomic force microscopy (AFM) and electron microscopy (EM).

An updated version for AFM can be found in the septinNetworkAFM repository.

Folders:
  AFM/mainFindHeight.py: Finds the average Height above the membrane surface by fitting the sum of two Gaussians to the height distribution.
  AFM/mainWidthBundles.py: Estimates the width of the bundles using mainly morphological operations.
  AFM/acf_image.py: Estimates the autocorrelation function
  TEM/mainIntervalDistanceFilamentArray.py: From filament coordinates of FJIJ code, get spacing between aligned filaments.
  TEM/resultsFigureEMAngleHistogram.py: From angle analysis in FIJI, plot distribution from angles using adapted Stack Overflow code.
  TEM/resultsFigureEMDistanceHistogram.py: Plot spacing between aligned filaments,
  TEM/resultsFigureEMOrientation.py: Get orientation information from image and show distribution.

Purpose:
For this theis we needed to quantifying filament network structure from AFM/EM images. For this, we extracted filament positions, measuring local order (spacing and angles between filaments), and distinguishing locally ordered clusters from globally disordered regions.
