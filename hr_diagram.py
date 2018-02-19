#!/usr/bin/python

#----------------------------------------------------------------------
#
# HR Diagram Module
#
# Takes Hipparcos website data directly as input through an ASCII
#  text file, and parses this into arrays for use in generating
#  an osberver's HR Diagram, ouput in PDF format.
#
# rtf: Last modified, 021918.
#----------------------------------------------------------------------

import string
import numpy as np
import matplotlib.pyplot as plt
import math

# Display all matplotlib commands inline in Jupyter
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')

# Global verbose flag ( = 1 for verbose output, 0 if not)
verbose = 0


#======================================================================
# absolute_magnitude:  Return absolute magnitude of a star given its
#  visual magnitude and parallax (in arcseconds). 
#  parallax (in arcseconds).
#
#======================================================================
#
#def absolute_magnitude (vmag, parallax):
#  Your code goes here
#  magnitude = 
#  return magnitude
#


#======================================================================
#
# is_number: Short routine to determine whether an input string is 
#  either a number or not -- returns True or False. Useful to clean out
#  empty or non-floating point entries from a data table.
#
#======================================================================

def is_number (s):

  try:
    float (s)
    return True

  except ValueError:
    return False


#======================================================================
#
# generate_plot: Generates an HR diagram in PDF format, given stellar
#  data input in ASCII format. Two strings are taken as arguments: 
#  the data file string inputfile, and the PDF output filename outputfile.
#
#  The data is assumed to be in column form,
#  divided by vertical bars, like so: 
#
#    HIP| Vmag|Plx|B-V
#
# where the HIP column is the integer Hipparcos HIP number for the star,
# Vmag is the stellar magnitude in Johnson V band filter, Plx is the 
# parallax _in milliarcseconds_, and B-V is the Jonson B-V band color. 
# The code converts to arcseconds for the parallax, displays the HR
# diagram to the Jupyter notebook, and outputs a PDF file with the 
# HR diagram.
#
#========================================================================= 

def generate_plot (inputfile, outputfile):

# Open data file for reading

  f = open (inputfile, 'r')

# Inititalize data lists

  stellarname = [] # List for HIP name
  MV = []          # List for V band magnitude
  bminusv = []     # List for B-V color

# Read data in line by line, parse it and store to data lists

  for line in f:

    if (verbose == 1) :
      print (line)

# Skip commented lines beginning with #
    if line.startswith("#") :
      pass

    else :
      lst = line.split ('|')  # split line into character fields
      if (len (lst) > 3) :
        namestr  = lst [0] # HIP name entry
        magstr   = lst [1] # V magnitude entry
        parstr   = lst [2] # parallax (in mas) entry
        colorstr = lst [3] # B-V color entry

# Ensure all entries are valid floating point numbers, otherwise skip this line

        if (is_number (magstr) and is_number (colorstr) and is_number (parstr) ):
          parallax = float (parstr)

# Convert entries to floats, and append to data lists.

          if (parallax > 0.0) :
            parallax = parallax / 1.e3 # convert from to arcseconds
            vmag = float (magstr)
            MV.append (vmag)
#           absolute = absolute_magnitude (vmag, parallax)
#           MV.append (absolute)
            color = float (colorstr)
            bminusv.append (color)

# Generate plot. We set the V and B-V limits of the plot as well as the 
#  aspect ratio. Show to Jupyter notebook (see 'matplotlib inline') command
#  above, and also output to PDF file.

  plt.plot (bminusv, MV, 'ko', markersize = 1)
  plt.xlabel ('B Minus V Color')
  plt.ylabel ("V Magnitude")
  ax = plt.gca()
  plt.xlim (-0.5, 2.5)
  plt.ylim (-5, 20.)
  ax.set_ylim(ax.get_ylim()[::-1])
  ax.set_aspect(1./4.)
  plt.savefig (outputfile, format = 'pdf')
  plt.show()
