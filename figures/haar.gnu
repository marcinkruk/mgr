#!/usr/bin/gnuplot

#
# Code to produce HAAR wavelet example
#

# Housekeeping
set samples 1000

# Styles
set xzeroaxis linetype 1 linecolor black
set yzeroaxis linetype 1 linecolor black
# set arrow from 0,0 to 1.5,0 head nofilled 
unset border
set xtics axis 0,0.5,1 offset 1.5 font "cmr10"
set ytics axis -1,2,1 offset -0.5 font "cmr10"

# Labels
set title "Haar wavelet" font "cmr10"
unset key

# Ranges
set xrange [-0.5:1.5]
set yrange [-1.25:1.25]

# Define functions to plot a piecewise function
f(x) = x < 0 ? 1/0 : x < 0.5 ? 1 : 1/0
g(x) = x < 0.5 ? 1/0 : x < 1 ? -1 : 1/0
h(x) = x < 0 ? 0 : x < 1 ? 1/0 : 0

# vertical lines to  connect piercewise function
set arrow from 0,0 to 0,1 nohead dashtype 3 linecolor rgbcolor "#0080FF"
set arrow from 0.5,-1 to 0.5,1 nohead dashtype 3 linecolor rgbcolor "#0080FF"
set arrow from 1,-1 to 1,0 nohead dashtype 3 linecolor rgbcolor "#0080FF"

# PLOT
set term pngcairo
set output "haar.png"
plot \
f(x) lt 1 lw 2 lc rgbcolor "#0080FF",\
g(x) lt 1 lw 2 lc rgbcolor "#0080FF",\
h(x) lt 1 lw 2 lc rgbcolor "#0080FF"
