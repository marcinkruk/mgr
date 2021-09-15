#!/usr/bin/gnuplot

# Styles
set xzeroaxis linetype 1 linecolor black
set yzeroaxis linetype 1 linecolor black
# set arrow from 0,0 to 1.5,0 head nofilled 
unset border
set xtics axis 0,1,4 offset 1.5 font "cmr10"
set ytics axis 0.5,0.5,1.5 offset -0.5 font "cmr10"

# Labels
set title "db4 wavelet" font "cmr10"
unset key

# Ranges
set xrange [0:4.5]
set yrange [-0.2:1.6]

# vertical lines to points
set arrow from 1,0 to 1,0.6830127 nohead dashtype 3 linecolor rgbcolor "#0080FF"
set arrow from 2,0 to 2,1.1830127 nohead dashtype 3 linecolor rgbcolor "#0080FF"
set arrow from 3,0 to 3,0.3169873 nohead dashtype 3 linecolor rgbcolor "#0080FF"
set arrow from 4,0 to 4,-0.1830127 nohead dashtype 3 linecolor rgbcolor "#0080FF"

# PLOT
set term svg enhanced fontscale 2
set output "db4.svg"
plot "db4.data" u 1:2 pt 7 lc rgbcolor "#0080FF"
