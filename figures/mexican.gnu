#!/usr/bin/gnuplot -p

#
# Code to produce MEXICAN HAT wavelet example
#

# Housekeeping
set samples 1000

# Styles
set xzeroaxis linetype 1 linecolor black
set yzeroaxis linetype 1 linecolor black
# set arrow from 0,0 to 1.5,0 head nofilled 
unset border
set xtics axis (-4, -3, -2, -1, 1, 2, 3, 4) font "cmr10"
set ytics axis -1,2,1 font "cmr10"

# Labels
set title "Mexican hat wavelet" font "cmr10"
unset key

# Ranges
set xrange [-5:5]
set yrange [-0.5:1.1]

# Define functions
sigma = 1 
c = 2/(sqrt(3*sigma)*pi**(0.25))
f(x) = c * (1 - (x/sigma)**2) * exp(-x**2/(2*sigma**2))

# PLOT
set term pngcairo
set output "mexican.png"
plot \
f(x) lt 1 lw 2 lc rgbcolor "#0080FF"
