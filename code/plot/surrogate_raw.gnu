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
set title "Raw surrogate data" #font "cmr10"
#set key font "cmr10"
#set xtics font "cmr10"
#set ytics font "cmr10"

# Two Y axes
set ytics nomirror
set y2tics

# data ranges
set xrange ["1972-02-01":"2020-12-01"]
set key right top

# Axis labels
set xlabel "Years"
set ylabel "Oil price [USD]"
set y2label "U.S. Dollar index [arb. u.]"

# PLOT
set size ratio 0.5625
set term svg enhanced font "cmr10"
set output "surrogate_raw.svg"
plot \
"../output/00666/oil" u 1:2 \
axis x1y1 \
w l lc rgbcolor "#0080FF" \
title "U.S. crude oil price",\
"../output/00666/dollar" u 1:2\
w l lc rgbcolor "#FFA500" \
axis x1y2 \
title "U.S. Dollar index"

