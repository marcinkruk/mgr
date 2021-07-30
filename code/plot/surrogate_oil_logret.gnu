#!/usr/bin/gnuplot -p

#
#
#

# csv handling
set datafile separator ','

# Handle time on X axis
set xdata time
set timefmt "%Y-%m-%d"
set format x "%Y"

# title
set title "Surrogate oil log returns" #font "cmr10"

# data ranges
set xrange ["1972-02-01":"2020-12-01"]
unset key

# Axis labels
set xlabel "Years"

# PLOT
set size ratio 0.5625
set term svg enhanced font "cmr10"
set output "surrogate_oil_logret.svg"
plot \
"../output/01000/oil_with_log_returns.csv" u 1:3\
w l lc rgbcolor "#0080FF"
