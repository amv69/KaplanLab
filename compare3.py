import gzip
import sys
import os
import subprocess

fname = sys.argv[1]
fasta = sys.argv[2]


print(fname)
outFile = fname[:-9] + "_match.txt"
out = open(noneFile, "w+")
with open(fasta) as f2:
    fastaLines = f2.readlines()
    fastaReads = fastaLines[1::2]
    for read in fastaReads:
        read = read[26:-27]
        print("Searching for: " + str(read) + "\nin: " + str(fasta))
        command = "gunzip -c " + fname + " | grep -i -c " + str(read).strip('\'').strip('b\'').strip('\\n') + " >> " + outFile
        subprocess.call(command,shell=True) 
            #if read.lower() in map(str.lower, fastaReads):
                #subprocess.call(gsed -n '2~4p' , shell=True)
               # cmd = "grep -i -B 1 " + str(read).strip('\'').strip('b\'').strip('\\n') + " " + fasta + " | head -1 >> " + outFile
                #subprocess.call(cmd, shell=True)
