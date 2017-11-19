HUAP
=======
The Hurry Up And Plot (who-app) is an easy-to-use plotting tool to both create a summary of seeing throughout the Night, and visual plots for your enjoyment. This tool should already be in the DECamObserver directory.


Table of Contents:
==================

   * [HUAP](#HUAP)
   * [Table of Contents:](#table-of-contents)
   * [TL;DR](#tldr)
   * [Installation](#installation)
   * [Usage](#usage)
   * [HUAP Method](#HUAP-method)
   * [Dependencies](#dependencies)


TL;DR
=====

* Step 1 : Use the command qcInvPrint in the godb window on the Observer2 console in kentools.
* Step 2 : Open a new terminal and type "python HUAP.py"
* Step 3 : Read the terminal output to obtain the seeing summary, and view plots.

Installation
=============
This file should already be in the DECamObserver directory, if not view the Raw image of HUAP.py and right click and save as. 

Usage
======

HUAP is used in conjuction with the kentools command qcInvPrint. This grabs the observation data for the night and saves into the DECamObserver directory a "YYYYMMDD".qcinv file. The day seems to be given by when you run the code, so in general will be +1 to the actual observing night.

As this is dependent on kentools and qcInvPrint, in general you will need to be at the Observer2 station.

To run the program:

* Open a new Terminal
* Navigate to the directory "DECamObserver"
* Run python HUAP.py in the command line.

If you would like to know the optional arguments that can be parsed you can use the help option "-h, --help".

Current arguments are:

* --Date, --D : Set the date of the input file. Takes the form YYYY-MM-DD. Default is the current day (not observing night).
* --show-plots : A boolean argument that can be parsed to show the two summary plots for psf and t_eff. Default is "False".


If you run HUAP with 20171119.qcinv file in the same directory, you should be able to reproduce the figures included in the repository. Remember that you should rename the plot files or the will be overwritten.

HUAP Method
===============
The program itself is currently limited to producting psf and t_eff plots against time. The information is read in from qcInvPrint file.

Currently the program also breaks the night into 4 quarters based on the start and end times contained in the input file. In the future it is hoped that if can take an argument to decide how many quartiles are needed when DES only observed for half the night.This quartering is simply a partitioning of the data into 4 equal length time bands.

The data is then manipulated to produce the following plots:

* all-band_psf.png : Entire night summary of the psf including bands ugrizY.
* all-band_t_eff.png : Entire night summary of the t_eff including bands ugrizY.
* Q(n)-all_band_psf.png : nth quartile night summary of the psf including bands ugrizY.
* Q(n)-all_band_t_eff.png : nth quartile night summary of the t_eff including bands ugrizY.

For the above plots, included in the legend are the median psf/t_eff and plotted median lines.
Additionally, the mean, median and RMSD are calculated and outputted into the terminal. This is aimed to make filling in the CTIO Night Report easier, especially for those not comfortable with SQL.

Dependencies
============

* Python 2.7
	* Numpy
	* Matplotlib
	* Datetime
	* os
	* system
	* warnings
	* argparse

Relies upon kentools:
* qcInvPrint

For more information on the kentools package please see : https://cdcvs.fnal.gov/redmine/projects/desops/wiki/Introduction_to_kentools

Kentools was created by Steve Kent.

