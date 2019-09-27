import re
import os
import csv
import sys
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt

sns.set()
dir = sys.argv[1]
spliceSites = sys.argv[2]

diffs = []
binArray = list(range(-5, 100))
#Has to run in same directory that this paths to
for fname in os.listdir(dir):
    with open(fname) as f:
        bedData = [cols[0:3] for cols in csv.reader(f, delimiter="\t")]

    with open(spliceSites) as f:
        ss = [cols[0:2] for cols in csv.reader(f, delimiter="\t")]

    for row in bedData:
        del row[1]

    for line in bedData:
        for site in ss:
            if line[0] == site[0]:
                #Plus Strand
                diff = int(line[1]) - int(site[1])
                #Minus strand
                #diff = int(site[1]) - int(line[1])
                if -50 < diff < 100:
                    diffs.append((diff))
                    #diffs.append((site[0],site[1],diff)) Used for old Graphing Code
            elif line[0] != site[0]:
                pass

    out = np.array(diffs)
    #colorCode = sns.color_palette("Paired") #Unused, just for color changes
    graph = sns.distplot(out, kde=False, bins=np.arange(-5, 100)-0.5) #-0.5 Centers data on the x axis
    graph.set(xlabel='# of Bases', ylabel="# of Reads", title= "3' Pileup Relative to Splice Site")
    plt.legend()
    plt.savefig("/Users/Alex/Desktop/intronsPlus/graphsSKIPS/" + str(fname)[:-3] + "png")
    out = []
    diffs = []
    plt.clf()


#OLD GRAPHING CODE
#
#
#all = []
#for val in diffs:
#    all.append((val[0] + val[1]))

#temp = []
#all = list(dict.fromkeys(all))
#print(all)
#for site in all:
#    for val in diffs:
#        if site == (val[0] + val[1]):
#            temp.append(val[2])
#    out = np.array(temp)
#    plt.hist(out, binArray)
#    plt.title("3' Relative to SS for " + site + " - Strand")
#    plt.xlabel("# of Bases")
#    plt.ylabel("Total # of Reads")
#    plt.show()
#    out = []
#    temp = []
