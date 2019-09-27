import re
import os
import csv
import sys
import codecs
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt

dir = sys.argv[1] #Dir of bed files to graph
spliceSites = sys.argv[2]

diffs = []
binArray = list(range(-5, 100))
#Has to run in same directory that this paths to
for fname in os.listdir(dir):
    with open(fname) as f:
        bedData = [cols[0:3] for cols in csv.reader(f, delimiter="\t")] #Gets useful info from bed
    with open(spliceSites) as f:
        ss = [cols[0:2] for cols in csv.reader(f, delimiter="\t")] #useful SS info

    for row in bedData:
        del row[1]
    for site in ss:
        for line in bedData:
            if line[0] == site[0]:
                #Plus Strand
                #diff = int(line[1]) - int(site[1])
                #Minus strand
                diff = int(site[1]) - int(line[1])
                if -50 < diff < 100:
                    diffs.append((diff))
                    #diffs.append((site[0],site[1],diff)) Used for old Graphing Code
            elif line[0] != site[0]:
                pass

        out = np.array(diffs) #All of the graphing code, self explanatory
        graph = sns.distplot(out, kde=False, bins=np.arange(-5, 100)-0.5) #-0.5 Centers data on the x axis
        graph.set(xlabel='# of Bases', ylabel="# of Reads", title= "3' Pileup Relative to " + str(site[0]) + " " + str(site[1]))
        plt.savefig("/Users/Alex/Desktop/intronsMinus/graphsSKIPS/" + str(fname)[:-4] + str(site[0]) + str(site[1]))
        with open('/Users/Alex/Desktop/cigarsMinusSKIPS.txt', 'a+') as f:
            f.write(fname + " " + str(site[0]) + " " + str(site[1]))
            f.write(str(out) + "\n")
        out = []
        diffs = []
        plt.clf()

#        diffs2 = []
#        fname2 = re.sub('_R1_sce_', '_SKIPS_sce_', fname)
#        fname3 = '/Users/Alex/Work/netseq/newCigars/SKIPS/' + fname2
#        with open(fname3, encoding="utf8", errors='ignore') as f:
#            print(f)
#            bedData = [cols[0:3] for cols in csv.reader(f, delimiter="\t")]
#        with open(spliceSites) as f:
#            ss = [cols[0:2] for cols in csv.reader(f, delimiter="\t")]
#        for row in bedData:
#            del row[1]
#        for site in ss:
#            for line in bedData:
#                if line[0] == site[0]:
#                    #Plus Strand
#                    diff = int(line[1]) - int(site[1])
#                    #Minus strand
#                    #diff = int(site[1]) - int(line[1])
#                    if -6 < diff < 100:
#                        diffs2.append((diff))
#                        #diffs.append((site[0],site[1],diff)) Used for old Graphing Code
#                elif line[0] != site[0]:
#                    pass
#            f.close()


#            out2 = np.array(diffs2)
#            with open('/Users/Alex/Desktop/cigars.txt', 'w+') as f:
#                f.write(str(out))
#                f.write(str(out2))
#                f.close()
        #colorCode = sns.color_palette("Paired") #Unused, just for color changes
#            graph = sns.distplot(out2, kde=False, bins=np.arange(-5, 100)-0.5) #-0.5 Centers data on the x axis
#            graph.set(xlabel='# of Bases', ylabel="# of Reads", title= "3' Pileup Relative to " + str(site[0]) + " " + str(site[1]))
        #plt.legend()
#            plt.savefig("/Users/Alex/Desktop/intronsPlus/graphsSKIPS/" + str(fname3)[45:-4] + str(count) + ".png")
#            out = []
#            diffs = []
#            plt.clf()
#            out2 = []
#            diffs2 = []
#            count = count + 1



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
