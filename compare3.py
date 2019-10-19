import gzip
import sys
import os
import subprocess

fname = sys.argv[1]
fasta = sys.argv[2]


print(fname)
outFile = fname[:-9] + "_match.txt"
missFile = fname[:-9] + "_miss.txt"
noneFile = fname[:-9] + "_none.txt"
out = open(noneFile, "w+")
with gzip.open(fname) as f:
    lines = f.readlines()
    reads = lines[1::4]
    with open(fasta) as f2:
        fastaLines = f2.readlines()
        fastaReads = lines[1::2]
        for read in reads:
            if read in fastaReads:
                #subprocess.call(gsed -n '2~4p' , shell=True)
                cmd = "grep -i -B 1 " + str(read).strip('\'').strip('b\'').strip('\\n') + " " + fasta + " | head -1 >> " + outFile
                subprocess.call(cmd, shell=True)
            else:
                out.write(read)
        subprocess.call("uniq -u " + outFile + "> uniq_" + outFile, shell=True)
        subprocess.call("sed '2~2d' " + fasta + "> names_" + fasta, shell=True)
        subprocess.call("diff names_" + fasta + "uniq_" + outFile + "> " + missFile)
        out.close()
