#!/usr/bin/python

import numpy
import pandas
import pywt

def filter_wavelets(arr, n):
	tmp=arr.copy()
	for i in range(len(tmp)):
		if i != n:
			tmp[i]=numpy.zeros_like(tmp[i])
	return tmp

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

#print(dollar_data)
#print(oil_data)

# Wavelet transform
oil_wavedec=pywt.wavedec(oil_data.log_return[1:], 'db4', mode='zero')
dollar_wavedec=pywt.wavedec(dollar_data.log_return[1:], 'db4', mode='zero')

#print(oil_wavedec)
#print(dollar_wavedec)

# Multi-resolution analysis
oil_wr_0=pywt.waverec(filter_wavelets(oil_wavedec,0), 'db4', mode='zero')
oil_wr_1=pywt.waverec(filter_wavelets(oil_wavedec,1), 'db4', mode='zero')
oil_wr_2=pywt.waverec(filter_wavelets(oil_wavedec,2), 'db4', mode='zero')
oil_wr_3=pywt.waverec(filter_wavelets(oil_wavedec,3), 'db4', mode='zero')
oil_wr_4=pywt.waverec(filter_wavelets(oil_wavedec,4), 'db4', mode='zero')
oil_wr_5=pywt.waverec(filter_wavelets(oil_wavedec,5), 'db4', mode='zero')
oil_wr_6=pywt.waverec(filter_wavelets(oil_wavedec,6), 'db4', mode='zero')

#print(oil_wr_0)
#print(oil_wr_1)
#print(oil_wr_2)
#print(oil_wr_3)
#print(oil_wr_4)
#print(oil_wr_5)
#print(oil_wr_6)

dollar_wr_0=pywt.waverec(filter_wavelets(dollar_wavedec,0), 'db4', mode='zero')
dollar_wr_1=pywt.waverec(filter_wavelets(dollar_wavedec,1), 'db4', mode='zero')
dollar_wr_2=pywt.waverec(filter_wavelets(dollar_wavedec,2), 'db4', mode='zero')
dollar_wr_3=pywt.waverec(filter_wavelets(dollar_wavedec,3), 'db4', mode='zero')
dollar_wr_4=pywt.waverec(filter_wavelets(dollar_wavedec,4), 'db4', mode='zero')
dollar_wr_5=pywt.waverec(filter_wavelets(dollar_wavedec,5), 'db4', mode='zero')
dollar_wr_6=pywt.waverec(filter_wavelets(dollar_wavedec,6), 'db4', mode='zero')

# Represent as pandas DataFrame
oil_wr=pandas.DataFrame()
oil_wr['0']=oil_wr_0
oil_wr['1']=oil_wr_1
oil_wr['2']=oil_wr_2
oil_wr['3']=oil_wr_3
oil_wr['4']=oil_wr_4
oil_wr['5']=oil_wr_5
oil_wr['6']=oil_wr_6

dollar_wr=pandas.DataFrame()
dollar_wr['0']=dollar_wr_0
dollar_wr['1']=dollar_wr_1
dollar_wr['2']=dollar_wr_2
dollar_wr['3']=dollar_wr_3
dollar_wr['4']=dollar_wr_4
dollar_wr['5']=dollar_wr_5
dollar_wr['6']=dollar_wr_6

# Output to csv
dollar_wr.to_csv('./output/dollar_wr.csv')
oil_wr.to_csv('./output/oil_wr.csv')

