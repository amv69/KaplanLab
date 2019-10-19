import gzip
import sys
import os
import subprocess

fname = sys.argv[1]
fasta = sys.argv[2]


print(fname)
outFile = fname[:-9] + "_match.txt"
with open(fasta) as f2:
    fastaLines = f2.readlines()
    fastaReads = fastaLines[1::2]
    for read in fastaReads:
        read = read[26:-27]
        command = "gunzip -c " + fname + " | grep -i -c " + str(read).strip('\'').strip('b\'').strip('\\n') + " >> " + outFile
        subprocess.call(command,shell=True)
