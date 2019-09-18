import re
import sys
import numpy as np
import matplotlib.pyplot as plt

filename = sys.argv[1]

with open(filename) as f:
    data = f.readlines()

for n, line in enumerate(data, 1):
    print '{:2}.'.format(n), line.rstrip()

print '-----------------'
