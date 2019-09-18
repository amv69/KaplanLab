import re
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2
import matplotlib.pyplot as plt3

filename = sys.argv[1]

with open(filename) as f:
    data = f.readlines()

for n, line in enumerate(data, 1):
    print '{:2}.'.format(n), line.rstrip()

print '-----------------'

cigarList = [] #Temp
cigarList2 = [] #Temp
cigarList3 = [] #Post Skip
cigarList4 = [] #Pre Skip
cigarList5 = [] #Skips
binArray = list(range(10))
for cigar in data:
    cigarList.append(cigar.split('M', 1))

for cigar in cigarList:
    cigar[0] = cigar[0].split('S', 1)[-1]
    cigar[1] = cigar[1].split('N', 1)
    cigarList2.append((cigar[0], cigar[1][0], cigar[1][1]))

for cigar in cigarList2[:]:
    if str(cigar[1]).find("D") != -1:
        cigarList2.remove(cigar)
    cigarList3.append(cigar[2].split('M', 1)[0]) #After Skip

for cigar in cigarList2[:]:
    cigarList4.append(cigar[0]) #Pre Skip
    cigarList5.append(cigar[1]) #skips

preSkips = np.array(cigarList4)
postSkips = np.array(cigarList3)
skips = np.array(cigarList5)
#Post Skips
plt.hist(postSkips, binArray)
plt.title("postSkips")
plt.xlabel("# of Reads After Skip")
plt.ylabel("Total # of Reads")
plt.show()

#Pre Skips
plt2.hist(preSkips, binArray)
plt2.title("preSkips")
plt2.xlabel("# of Reads Before Skip")
plt2.ylabel("Total # of Reads")
plt2.show()

#Skips
plt3.hist(skips, binArray)
plt3.title("skips")
plt3.xlabel("# of Reads In Skip")
plt3.ylabel("Total # of Reads")
plt3.show()
