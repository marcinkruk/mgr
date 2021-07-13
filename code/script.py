#!/usr/bin/python

import numpy
import pandas
import pywt

# Import input files
dollar_data=pandas.read_csv("./input_data/TWEXMMTH.csv")
oil_data=pandas.read_csv("./input_data/oil.csv")

# Create surrogate by shuffling
if False: # TODO: have it shuffle conditionally
    numpy.random.shuffle(dollar_data.TWEXMMTH.to_numpy())
    numpy.random.shuffle(oil_data.usd.to_numpy())

# Calculate log returns
dollar_data["log_return"]=numpy.log(dollar_data.TWEXMMTH) - numpy.log(dollar_data.TWEXMMTH.shift(1))
oil_data["log_return"]=numpy.log(oil_data.usd) - numpy.log(oil_data.usd.shift(1))

print(dollar_data)
print(oil_data)

# Wavelet transform
#wavelet_basis = pywt.Wavelet('db4')
