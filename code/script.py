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
import matplotlib.pyplot as plt
from mgrtools import GcDataStructure

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

    # Prepare directory for output
    outputdir='./output/'+format(counter, '05d')
    os.mkdir(outputdir)

    # Output raw data
    dollar.to_csv(outputdir+'/dollar', header=None, index=None)
    oil.to_csv(outputdir+'/oil', header=None, index=None)

    # Output wavelet reconstucted data to prepare files for Diks-Panchenko GC test
    for col_usd in dollar_wr.iteritems():
        for col_oil in oil_wr.iteritems():
            c_oil=col_oil[0]
            c_usd=col_usd[0]

            dollar_file=outputdir+'/dollar_wr_'+c_usd
            oil_file=outputdir+'/oil_wr_'+c_oil
            dollar_wr[c_usd].to_csv(dollar_file, header=None, index=None)
            oil_wr[c_oil].to_csv(oil_file, header=None, index=None)

    # res is an BAND_USD x BAND_OIL x STEP array of GC test results
    res=numpy.ndarray(shape=(7,7,6), dtype=GcDataStructure)
    for i in range(7):
        for j in range(7):
            for k in range(6):
                res[i][j][k]=GcDataStructure()

    print("step, usd->oil, oil->usd", file=open(outputdir+'/p_values', 'a'))
    for col_usd in dollar_wr.iteritems():
        for col_oil in oil_wr.iteritems():
            c_oil=col_oil[0]
            c_usd=col_usd[0]
            print("Band: usd " + c_usd + " oil " + c_oil, file=open(outputdir+'/p_values', 'a'))

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
                res[int(c_usd)][int(c_oil)][n].set_linear(linear_p_val[n])

            # Calculate nonlinear GC
            dollar_file=outputdir+'/dollar_wr_'+c_usd
            oil_file=outputdir+'/oil_wr_'+c_oil

            print("Nonlinear p-values:", file=open(outputdir+'/p_values', 'a'))
            for n in range(1, 7):
                nonlinear_p_val=dp_test(dollar_file, oil_file, n)
                print(str(n) + ", " + str(nonlinear_p_val[0]) + ", " + str(nonlinear_p_val[1]), file=open(outputdir+'/p_values', 'a'))
                res[int(c_usd)][int(c_oil)][n-1].set_nonlinear(nonlinear_p_val)

    return res

# Import input files
dollar_data=pandas.read_csv("./input_data/TWEXMMTH.csv")
oil_data=pandas.read_csv("./input_data/oil.csv")

counter=0

results=[]
n_iterations=1001
for i in range(n_iterations):
    print("Iteration number: " + str(i))
    results.append(analyze(dollar_data, oil_data))
    dollar_data.TWEXMMTH=surrogate_fourier_phases(dollar_data.TWEXMMTH)
    oil_data.usd=surrogate_fourier_phases(oil_data.usd)
    counter+=1

# Data structure to hold number of success in surrogate data
surrogate_success=numpy.ndarray(shape=(7,7,6), dtype=GcDataStructure)
for i in range(7):
    for j in range(7):
        for k in range(6):
            surrogate_success[i][j][k]=GcDataStructure()

print("Aggregating surrogate results...")
treshold=0.05
for b1 in range(7):
    for b2 in range(7):
        for s in range(6):
            for n in range(1,n_iterations):
                if results[n][b1][b2][s].linear_usd_oil < treshold:
                    surrogate_success[b1][b2][s].linear_usd_oil+=1
                if results[n][b1][b2][s].linear_oil_usd < treshold:
                    surrogate_success[b1][b2][s].linear_oil_usd+=1
                if results[n][b1][b2][s].nonlinear_usd_oil < treshold:
                    surrogate_success[b1][b2][s].nonlinear_usd_oil+=1
                if results[n][b1][b2][s].nonlinear_oil_usd < treshold:
                    surrogate_success[b1][b2][s].nonlinear_oil_usd+=1

print("Print them out and we're done!")
print("linear: usd->oil, oil->usd, nonlinear: usd->oil, oil->usd", file=open('./output/surrogate_results', 'a'))
for b1 in range(7):
    for b2 in range(7):
        print("band usd: " + str(b1) + " band oil: " + str(b2), file=open('./output/surrogate_results', 'a'))
        for s in range(6):
            surrogate_success[b1][b2][s].linear_usd_oil/=n_iterations-1
            surrogate_success[b1][b2][s].linear_oil_usd/=n_iterations-1
            surrogate_success[b1][b2][s].nonlinear_usd_oil/=n_iterations-1
            surrogate_success[b1][b2][s].nonlinear_oil_usd/=n_iterations-1
            print(str(s) \
                + ", " + str(surrogate_success[b1][b2][s].linear_usd_oil) \
                + ", " + str(surrogate_success[b1][b2][s].linear_oil_usd) \
                + ", " + str(surrogate_success[b1][b2][s].nonlinear_usd_oil) \
                + ", " + str(surrogate_success[b1][b2][s].nonlinear_oil_usd), \
                file=open('./output/surrogate_results', 'a'))

