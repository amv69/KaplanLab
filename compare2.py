import gzip
import sys
import os
import subprocess

fname = sys.argv[1]
fasta = sys.argv[2]


print(fname)
outFile = fname[:-4] + "_match.txt"
missFile = fname[:-4] + "_miss.txt"
with gzip.open(fname) as f:
    lines = f.readlines()
    reads = lines[1::4]
    with open(fasta) as f2:
        fastaLines = f2.readlines()
        fastaReads = lines[1::2]
        for fastaRead in fastaReads:
            if fastaRead in reads:
                cmd = "grep -i -B 1 " + str(fastaRead).strip('\'').strip('b\'').strip('\\n') + " " + fasta + " | head -1 >> " + outFile
                subprocess.call(cmd, shell=True)
        subprocess.call("uniq -u " + outFile + "> uniq_" + outFile, shell=True)
        subprocess.call("sed '2~2d' " + fasta + "> names_" + fasta, shell=True)
        subprocess.call("diff names_" + fasta + "uniq_" + outFile + "> " + missFile)
