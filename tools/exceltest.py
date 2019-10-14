#!/usr/bin/env python3

import csv
import os

# dir_path = os.path.dirname(os.path.realpath(__file__))
# open(dir_path + '/' + 'lbd_fvp_b1l.csv')

# open('tools/lbd_fvp_b1l.csv', newline='')
with open('tools/lbdheadertemplate.csv', newline='') as csvfile:
    fvpreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in fvpreader:
        print(', '.join(row))