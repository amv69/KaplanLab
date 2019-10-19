import gzip
import sys
import os
import subprocess

pyCode = sys.argv[1]
dir = sys.argv[2]
fasta = sys.argv[3]

for fname in os.listdir(dir):
    cmd = "python3 " + pyCode + " " + fname + " " + fasta
    subprocess.Popen(cmd, shell=True)
    print("Started: " + cmd)
