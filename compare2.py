import gzip
import sys
import os
import subprocess

fname = sys.argv[1]
fasta = sys.argv[2]

outFile = fname[:-3] + "_match.txt"
missFile = fname[:-3] + "_miss.txt"
noneFile = fname[:-3] + "_noMatch.txt"
with gzip.open(fname) as f:
    lines = f.readlines()
    reads = lines[1::4]
    with open(fasta, "r") as f2:
        fastaLines = f2.readlines()
        fastaReads = fastaLines[1::2]
        for fastaRead in fastaReads:
            if fastaRead in reads:
                #Add Writing Mismatches not just what didnt mismatch
                cmd = "grep -i -B 1 " + str(fastaRead).strip('\'').strip('b\'').strip('\\n') + " " + fasta + " | head -1 >> " + outFile
                subprocess.call(cmd, shell=True)
            else:
                cmd2 = "grep -i -B 1" + str(fastaRead).strip('\'').strip('b\'').strip('\\n') + " " + fasta + " >> " + noneFile
                subprocess.call(cmd2, shell=True)
        subprocess.call("uniq -u " + outFile + "> uniq_" + outFile, shell=True)
        subprocess.call("sed '2~2d' " + fasta + "> names_" + fasta, shell=True)
        subprocess.call("diff names_" + fasta + "uniq_" + outFile + "> " + missFile)
