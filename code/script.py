#!/usr/bin/python

import numpy
import pandas
import pywt
import subprocess
import os
import re
import time

def filter_wavelets(arr, n):
	tmp=arr.copy()
	for i in range(len(tmp)):
		if i != n:
			tmp[i]=numpy.zeros_like(tmp[i])
	return tmp

def shuffle_input(dollar, oil):
    numpy.random.shuffle(dollar.TWEXMMTH.to_numpy())
    numpy.random.shuffle(oil.usd.to_numpy())

def multiscale_wavelet(arr):
    # Wavelet transform
    wavedec=pywt.wavedec(arr.log_return[1:], 'db4', mode='zero')

    # Multiscale analysis
    wr=pandas.DataFrame()
    for n in range(len(wavedec)):
        wr[str(n)]=pywt.waverec(filter_wavelets(wavedec,n), 'db4', mode='zero')

    return wr

def dp_test(file1, file2, d):
    dp_out=subprocess.check_output(['./GCTest', file1, file2, str(d), '1.4'])
    dp_p_val=[]

    pattern=re.compile('p-value=\d\.[\d]*')
    for line in dp_out.decode().split('\n'):
        match=pattern.findall(line)
        p_val=re.sub('[\[\]\']', '', re.sub('p-value=', '', str(match)))
        if len(p_val) != 0:
            dp_p_val.append(float(p_val))

    return dp_p_val

def analyze(arr1, arr2):
    dollar=arr1.copy()
    oil=arr2.copy()

    # Calculate log returns
    dollar["log_return"]=numpy.log(dollar.TWEXMMTH) - numpy.log(dollar.TWEXMMTH.shift(1))
    oil["log_return"]=numpy.log(oil.usd) - numpy.log(oil.usd.shift(1))

    # Multi-resolution analysis
    dollar_wr=multiscale_wavelet(dollar[1:])
    oil_wr=multiscale_wavelet(oil[1:])

    outputdir='./output/'+format(counter, '05d')
    os.mkdir(outputdir)

    band_arr=[]
    for col in oil_wr.iteritems():
        c=col[0]
        dollar_file=outputdir+'/dollar_wr_'+c
        oil_file=outputdir+'/oil_wr_'+c
        dollar_wr[c].to_csv(dollar_file, header=None, index=None)
        oil_wr[c].to_csv(oil_file, header=None, index=None)
        step_arr=[]
        for n in range(1, 7):
            step_arr.append(dp_test(dollar_file, oil_file, n))

        band_arr.append(step_arr)


    # Call linear GC
    # Parse output

    return band_arr

# Import input files
dollar_data=pandas.read_csv("./input_data/TWEXMMTH.csv")
oil_data=pandas.read_csv("./input_data/oil.csv")

counter=0

results=[]
for i in range(100):
    print("Iteration number: " + str(i))
    results.append(analyze(dollar_data, oil_data))
    shuffle_input(dollar_data, oil_data)
    counter+=1

#print(len(results))
#print(len(results[0]))
#print(len(results[0][0]))
#print(len(results[0][0][0]))
