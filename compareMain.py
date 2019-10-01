import gzip
import sys
import os
import subprocess

dir = sys.argv[1]
fasta = sys.argv[2]

for fname in os.listdir(dir):
    subprocess.Popen("python3 ~/Documents/Github/KaplanLab/compare2.py " + fname + " " + fasta, shell=True)
