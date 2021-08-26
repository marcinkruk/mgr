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

# Y zero axis
#set xzeroaxis ls 1 lc 'black' 

# title
set title "Surrogate USD: D2"

# data ranges
set xrange ["1972-02-01":"2020-12-01"]
unset key

# Axis labels
set xlabel "Years"

# PLOT
set size ratio 0.5625
set term svg enhanced font "cmr10"
set output "surrogate_usd_wr_D2.svg"
plot \
"../output/01000/dollar_with_log_returns.csv" u 1:3\
w l lc rgbcolor "#C0C0C0", \
"../output/01000/dollar_wr_5" u 1:2 \
w l lc rgbcolor "#0080FF"
