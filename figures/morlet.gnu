#!/usr/bin/gnuplot -p

#
# Code to produce MORLET wavelet example
#

# Housekeeping
set samples 1000

# Styles
set xzeroaxis linetype 1 linecolor black
set yzeroaxis linetype 1 linecolor black
# set arrow from 0,0 to 1.5,0 head nofilled 
unset border
set xtics axis -1,2,1 font "cmr10"
set ytics axis -1,2,1 font "cmr10"

# Labels
set title "Morlet wavelet" font "cmr10"
unset key

# Ranges
set xrange [-1.1:1.1]
set yrange [-1.1:1.1]

# Define functions
s = 4
sigma = 10
k = exp(-0.5 * sigma**2)
c = sqrt(1 + exp(- sigma**2) - 2 * exp(-0.75 * sigma**2))
i = {0.0, 1.0}

f(x) = c * pi**(-0.25) * exp(-0.5 * (s*x)**2) * (exp(i*sigma*s*x) - k)


# PLOT
set term pngcairo
set output "morlet.png"
plot \
real(f(x)) lt 1 lw 2 lc rgbcolor "#0080FF"
