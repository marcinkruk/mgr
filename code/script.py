#!/usr/bin/python

import numpy
import pandas
import pywt
import subprocess
import os
import random
import re
import time
import math
import cmath
from statsmodels.tsa.stattools import grangercausalitytests
from scipy.fft import fft, ifft

def filter_wavelets(arr, n):
	tmp=arr.copy()
	for i in range(len(tmp)):
		if i != n:
			tmp[i]=numpy.zeros_like(tmp[i])
	return tmp

def shuffle_input(dollar, oil):
    numpy.random.shuffle(dollar.TWEXMMTH.to_numpy())
    numpy.random.shuffle(oil.usd.to_numpy())

def shift_phase(n):
    return n*cmath.exp((0.0+1.0j)*random.uniform(0, 2*math.pi))

def surrogate_fourier_phases(arr):
    ft=fft(arr.to_numpy())
    ft[0]=shift_phase(ft[0])
    for n in range(1, (len(arr)+1)//2):
        ft[n]=shift_phase(ft[n])
        ft[len(arr)-n]=numpy.conj(ft[n])

    if (len(arr)%2) == 0:
        ft[len(arr)//2]=shift_phase(ft[len(arr)//2])

    surrogate=ifft(ft)

    # Return value has to be shifted to positive vales, because later log is computed.
    return surrogate.real + numpy.absolute(numpy.amin(surrogate.real)) + 1.0

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

def linear_gc(arr):
    result=grangercausalitytests(arr, 6, verbose=False)
    p_val=[]
    for n in range(1,7):
        p_val.append(result.get(n)[0].get('params_ftest')[1])

    return p_val


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

    linear_band=[]
    nonlinear_band=[]
    print("step, usd->oil, oil->usd", file=open(outputdir+'/p_values', 'a'))
    for col_oil in oil_wr.iteritems():
        for col_usd in dollar_wr.iteritems():
            c_oil=col_oil[0]
            c_usd=col_usd[0]
            print("Band: oil " + c_oil + " usd " + c_usd, file=open(outputdir+'/p_values', 'a'))

            # Prepare arrays for linear GC test
            data_linear_oil_dollar=pandas.concat([dollar_wr[c_usd], oil_wr[c_oil]], axis=1, join='inner')
            data_linear_dollar_oil=pandas.concat([oil_wr[c_oil], dollar_wr[c_usd]], axis=1, join='inner')

            # Calculate linear GC
            linear_oil_dollar=linear_gc(data_linear_oil_dollar)
            linear_dollar_oil=linear_gc(data_linear_dollar_oil)
            linear_p_val=list(zip(linear_dollar_oil, linear_oil_dollar))
            print("Linear p-values:", file=open(outputdir+'/p_values', 'a'))
            for n in range(len(linear_p_val)):
                print(str(n+1) + ", " + str(linear_p_val[n][0]) + ", " + str(linear_p_val[n][1]), file=open(outputdir+'/p_values', 'a'))
            linear_band.append(linear_p_val)

            # Prepare files for Diks-Panchenko GC test
            dollar_file=outputdir+'/dollar_wr_'+c_usd
            oil_file=outputdir+'/oil_wr_'+c_oil
            dollar_wr[c_usd].to_csv(dollar_file, header=None, index=None)
            oil_wr[c_oil].to_csv(oil_file, header=None, index=None)

            # Calculate nonlinear GC
            nonlinear_step=[]
            print("Nonlinear p-values:", file=open(outputdir+'/p_values', 'a'))
            for n in range(1, 7):
                nonlinear_p_val=dp_test(dollar_file, oil_file, n)
                print(str(n) + ", " + str(nonlinear_p_val[0]) + ", " + str(nonlinear_p_val[1]), file=open(outputdir+'/p_values', 'a'))
                nonlinear_step.append(nonlinear_p_val)

            nonlinear_band.append(nonlinear_step)

    return (linear_band, nonlinear_band)

# Import input files
dollar_data=pandas.read_csv("./input_data/TWEXMMTH.csv")
oil_data=pandas.read_csv("./input_data/oil.csv")

counter=0

linear_results=[]
nonlinear_results=[]
n_iterations=1000
for i in range(n_iterations):
    print("Iteration number: " + str(i))
    result=analyze(dollar_data, oil_data)
    linear_results.append(result[0])
    nonlinear_results.append(result[1])
    dollar_data=surrogate_fourier_phases(dollar_data)
    oil_data=surrogate_fourier_phases(oil_data)
    counter+=1


treshold=0.1
linear_surrogate_success_percent=[[[0 for p in range(2)] for s in range(6)] for b in range(7)]
nonlinear_surrogate_success_percent=[[[0 for p in range(2)] for s in range(6)] for b in range(7)]
for b in range(7):
    for s in range(6):
        for n in range(1,n_iterations):
            if linear_results[n][b][s][0] < treshold:
                linear_surrogate_success_percent[b][s][0]+=1
            if linear_results[n][b][s][1] < treshold:
                linear_surrogate_success_percent[b][s][1]+=1
            if nonlinear_results[n][b][s][0] < treshold:
                nonlinear_surrogate_success_percent[b][s][0]+=1
            if nonlinear_results[n][b][s][1] < treshold:
                nonlinear_surrogate_success_percent[b][s][1]+=1

print("linear: usd->oil, oil->usd, nonlinear: usd->oil, oil->usd", file=open('./output/surrogate_results', 'a'))
for b in range(7):
    print("band: " + str(b), file=open('./output/surrogate_results', 'a'))
    for s in range(6):
        linear_surrogate_success_percent[b][s][0]/=n_iterations-1
        linear_surrogate_success_percent[b][s][1]/=n_iterations-1
        nonlinear_surrogate_success_percent[b][s][0]/=n_iterations-1
        nonlinear_surrogate_success_percent[b][s][1]/=n_iterations-1
        print(str(s) \
                + ", " + str(linear_surrogate_success_percent[b][s][0]) \
                + ", " + str(linear_surrogate_success_percent[b][s][1]) \
                + ", " + str(nonlinear_surrogate_success_percent[b][s][0]) \
                + ", " + str(nonlinear_surrogate_success_percent[b][s][1]), \
                file=open('./output/surrogate_results', 'a'))

print(len(linear_results))
print(len(linear_results[0]))
print(len(linear_results[0][0]))
print(len(linear_results[0][0][0]))

print(len(nonlinear_results))
print(len(nonlinear_results[0]))
print(len(nonlinear_results[0][0]))
print(len(nonlinear_results[0][0][0]))
