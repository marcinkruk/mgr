#!/usr/bin/python

import numpy
import pandas
import pywt
import subprocess
import os

def filter_wavelets(arr, n):
	tmp=arr.copy()
	for i in range(len(tmp)):
		if i != n:
			tmp[i]=numpy.zeros_like(tmp[i])
	return tmp

def shuffle_input(dollar, oil):
    numpy.random.shuffle(dollar.TWEXMMTH.to_numpy())
    numpy.random.shuffle(oil.usd.to_numpy())

def analyze(arr1, arr2):
    print('counter is: '+str(counter))
    dollar=arr1.copy()
    oil=arr2.copy()

    # Calculate log returns
    dollar["log_return"]=numpy.log(dollar.TWEXMMTH) - numpy.log(dollar.TWEXMMTH.shift(1))
    oil["log_return"]=numpy.log(oil.usd) - numpy.log(oil.usd.shift(1))

    # Wavelet transform
    oil_wavedec=pywt.wavedec(oil.log_return[1:], 'db4', mode='zero')
    dollar_wavedec=pywt.wavedec(dollar.log_return[1:], 'db4', mode='zero')

    # Multi-resolution analysis
    oil_wr=pandas.DataFrame()
    oil_wr['0']=pywt.waverec(filter_wavelets(oil_wavedec,0), 'db4', mode='zero')
    oil_wr['1']=pywt.waverec(filter_wavelets(oil_wavedec,1), 'db4', mode='zero')
    oil_wr['2']=pywt.waverec(filter_wavelets(oil_wavedec,2), 'db4', mode='zero')
    oil_wr['3']=pywt.waverec(filter_wavelets(oil_wavedec,3), 'db4', mode='zero')
    oil_wr['4']=pywt.waverec(filter_wavelets(oil_wavedec,4), 'db4', mode='zero')
    oil_wr['5']=pywt.waverec(filter_wavelets(oil_wavedec,5), 'db4', mode='zero')
    oil_wr['6']=pywt.waverec(filter_wavelets(oil_wavedec,6), 'db4', mode='zero')

    dollar_wr=pandas.DataFrame()
    dollar_wr['0']=pywt.waverec(filter_wavelets(dollar_wavedec,0), 'db4', mode='zero')
    dollar_wr['1']=pywt.waverec(filter_wavelets(dollar_wavedec,1), 'db4', mode='zero')
    dollar_wr['2']=pywt.waverec(filter_wavelets(dollar_wavedec,2), 'db4', mode='zero')
    dollar_wr['3']=pywt.waverec(filter_wavelets(dollar_wavedec,3), 'db4', mode='zero')
    dollar_wr['4']=pywt.waverec(filter_wavelets(dollar_wavedec,4), 'db4', mode='zero')
    dollar_wr['5']=pywt.waverec(filter_wavelets(dollar_wavedec,5), 'db4', mode='zero')
    dollar_wr['6']=pywt.waverec(filter_wavelets(dollar_wavedec,6), 'db4', mode='zero')

    outputdir='./output/'+format(counter, '05d')
    os.mkdir(outputdir)
    for col in oil_wr.iteritems():
        c=col[0]
        oil_wr[c].to_csv(outputdir+'/oil_wr_'+c, header=None, index=None)
        dollar_wr[c].to_csv(outputdir+'/dollar_wr_'+c, header=None, index=None)

    # Call Diks-Panchenko code
    # Parse output

    # Call linear GC
    # Parse output

    # Cleanup
    del oil
    del dollar
    del oil_wavedec
    del dollar_wavedec
    del oil_wr
    del dollar_wr

    return None

# Import input files
dollar_data=pandas.read_csv("./input_data/TWEXMMTH.csv")
oil_data=pandas.read_csv("./input_data/oil.csv")

counter=0

for i in range(10):
    analyze(dollar_data, oil_data)
    shuffle_input(dollar_data, oil_data)
    counter+=1

