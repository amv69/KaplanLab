import sys
import csv

f1 = sys.argv[1]
f2 = sys.argv[2]
with open(f1) as f:
    with open('test.csv', 'w+') as csvfile:
        csvWriter = csv.writer(csvfile)
        csvWriter.writerow(["Chromosome Name", "Pileup"])
        for line in f:
            newLines = line.replace(']', '[').split('[')
            print(newLines[0])
            try:
                csvWriter.writerow([newLines[0], newLines[1]])

            except IndexError:
                print("haha")
