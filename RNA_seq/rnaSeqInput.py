import os
import sys
import subprocess

#Print statement to ensure that Conda environment has been activated or modules could be loaded with the script if a Job
#TO-DO Get versioning from conda/modules of all of the programs 
print("NOTE: This pipeline relies on reads being stored as *R1/R2 .fq (TO DO: add custom files)")
print("Ensure you are in prefered conda environment containing these tools:\n bamutil \n cutadapt \n samtools \n hisat2 \n fastx_toolkit \n bowtie2 \n bowtie \n sra-tools \n deeptools \n ucsc-bedgraphtobigwig \n debops \n fastqc \n ucsc-fetchchromsizes ")

#Wait command to ensure program will work correctly with given environment
#wait = input("Press Enter to Continue or Ctrl+C to Exit")

""" Used for Command line arguments instead of typing arguments as you go (Old?)

if(len(sys.argv) < 1): #Ensure that a path was given and if not alert user then exit
	print("Enter Absolute Path to reads after command")
	exit()

if(len(sys.argv) < 2):
	print("Enter absolute path to the genome after the reads location")
"""

#Setting up the given path to the reads
path = "~"
adaptThree = "~"
adaptFive = "~"
genome = "~"
hisatFile = "~"
spliceSites = "~" 
cut = "0"

while(True):
	path = input("Please enter absolute path to reads")
	if(os.path.exists(path) != True): #Checking to see if the path exists and if not then alert and exit
		print("Path does not exist")
		continue
	else:
		break

#Get current working directory so we can return
wd = os.getcwd()

#Move Working Directory to one specified with command line argument
os.chdir(path)

while(True):
	genome = input("Please enter absolute path to genome (FastA) file")
	if(os.path.exists(genome) != True): #Checking to see if the path exists and if not then alert and exit
		print("Path does not exist")
		continue
	else:
		break

while(True):
	hasIndex = input("Do you already have an indexed hisat file? (yes/no)")
	if(hasIndex.lower() != 'yes' or toIndex.lower() != 'no'):
		print('Please enter yes or no')
		continue
	else:
		break

#Genome file to index if there isn't an indexed genome
if(hasIndex == 'no'):
	hisatFile = input("Please enter index prefix")
	subprocess.check_call("hisat2-build " + genome + " " + hisatFile)
else:
	while(True):
		hisatFile = input("Please enter absolute path to index prefix")
		if(os.path.exists(hisatFile) != True): #Checking to see if the path exists and if not then alert and exit
			print("Path does not exist")
			continue 
			

#Have outside known splice sites or do them in file?
while(True):
	splice = input("Do you have a known splice site file? (yes/no)")
	if(splice.lower() != 'yes' or splice.lower() != 'no'):
		print('Please enter yes or no')
		continue
	else:
		break

if(splice == "yes"):
	while(True):
		spliceSites = input("Please enter absolute path to known splice sites \n NOTE:If not needed type none")
		if(splceSites.lower() == "none"):
			break
		if(os.path.exists(hisatFile) != True): #Checking to see if the path exists and if not then alert and exit
			print("Path does not exist")
			continue
		else:
			break

#Options for trimming 
while(True):
	print("Please Enter an option (1, 2 or 3)")
	print("1: Remove poly-A tails")
	print("2: Enter custom adapters to remove")
	print("3: Skip trimming")
	cut = input()
	if(cut != 1 or cut != 2 or cut != 3):
		print("Please enter 1, 2, or 3")
		continue

if(cut == 2):
	adaptThree = input("Please enter 3 prime Adapter to remove")
	adaptFive = input("Please enter 5 prime Adapter to remove")



#File path needed for fastqc, ensures that it exists and if not creates it
if(os.path.exists(path + "/fastqc_pretrim") != True):
        os.mkdir(path + "/fastqc_pretrim")

"""
The Subprocess calls needed that run all of the tools in the pipeline

There are multiple methods that can be chosen from for subprocess.METHOD()

Call() - Creates a subprocess and runs it, waits for previous child to complete
Check_Call() - if completes, just gives reutn code else it returns an actual error
Popen() - Creates an entirely new subprocess, waits for nothing (Used for tools that require no prior/post work)
Check_Output() - returns result as a byte string

shell = True - Makes subprocesses run in the shell

"""
#The fastqc calls for R1 & R2
subprocess.check_call("fastqc -o ./fastqc_pretrim/ *_R1.fastq", shell = True)
subprocess.check_call("fastqc -o ./fastqc_pretrim/ *_R2.fastq", shell = True)

if(cut == 1):
	#Cutadapt call for all R1 & R2 in current directory for poly-A tails
	subprocess.check_call("for f1 in *R1.fastq; do f2=${f1/R1/R2} && echo $f1 $f2; cutadapt -g XT{50} -A A{50}X -O 5 -o ${f1/.fastq/_cutadapt.fastq} -p ${f2/.fastq/_cutadapt.fastq} ${f1} ${f2} > ${f1/.fastq/cutadapt.txt}; done", shell = True)
elif(cut==2):
	#Cutadpat call for supplied adapters
	subprocess.check_call("for f1 in *R1.fastq; do f2=${f1/R1/R2} && echo $f1 $f2 cutadapt -a " + adaptThree + "X -g X" + adaptFive + "-O 5 -o ${f1/.fastq/_cutadapt.fastq} -p ${f2/.fastq/_cutadapt.fastq} ${f1} ${f2} > ${f1/.fastq/cutadapt.txt}; done", shell = True)

"""
The HISAT2 aligner is used here with fixed directories given for splicesites, the indexed genome and the output.

This can be updated to include inputable splicesites lcoation, genome (indexed or not) and change output dir

"""
if(splice == 'yes'):
	subprocess.check_call("for f1 in *R1_cutadapt.fastq; do f2=${f1/R1/R2} && echo $f1 $f2 && hisat2 -q --phred33 --max-intronlen 4000 --known-splicesite-infile --no-unal " + splceSites + " --rna-strandness RF --secondary --no-mixed --summary-file ${f1/R1_cutadapt.fastq/hs2.txt} -x " + hisatFile + " -1 ${f1} -2 ${f2} -S ${f1/R1_cutadapt.fastq/hs2.sam}; done", shell=True)

if(splice == 'no'):
	subprocess.check_call("for f1 in *R1_cutadapt.fastq; do f2=${f1/R1/R2} && echo $f1 $f2 && hisat2 -q --phred33 --max-intronlen 4000 --rna-strandness RF --secondary --no-mixed --summary-file ${f1/R1_cutadapt.fastq/hs2.txt} -x " + hisatFile + " -1 ${f1} -2 ${f2} -S ${f1/R1_cutadapt.fastq/hs2.sam}; done", shell=True)

#Call to convert SAM to BAM(-b) TO-DO: -S has been deprecated, make sure it works w/o
subprocess.check_call("for file in *hs2.sam; do echo $file && samtools view -S -b ${file} > ${file/sam/bam}; done", shell=True)

#Generate Headers fpr the BAM files and out put as X_header.sam
subprocess.check_call("for file in *bam; do echo $file && samtools view -H ${file} > ${file/.bam/_header.sam}; done", shell=True)

#Generate file of unique
subprocess.check_call('for f1 in *bam; do f2=${f1/.bam/_header.sam} && echo $f1 $f2 && samtools view ${f1} | grep -w "NH:i:1" | cat ${f2} - | samtools view -Sb - > ${f1/.bam/_unique.bam}; done', shell=True)

#sort unique reads
subprocess.check_call("for file in *unique.bam; do echo $file && samtools sort $file -o ${file/.bam/_sorted.bam} && rm $file; done", shell=True)

#index 
subprocess.check_call("for file in *sorted.bam; do echo $file && samtools index -b $file; done", shell=True)

subprocess.check_call("for file in *sorted.bam; do echo $file && samtools idxstats $file | cut -f 1 | grep -v chrM | xargs samtools view -b $file > ${file/.bam/_mt.bam}; done", shell=True)

subprocess.check_call("for file in *_unique_sorted_mt.bam; do echo $file && bedtools bamtobed -cigar -i $file > ${file/_unique_sorted_mt.bam/.bed}; done", shell=True)

#Get genomecoverage for bed files
subprocess.check_call('for str in "+" "-"; do [ "$str" = "+" ] && n="rev" || n="fw"; for file in *.bed; do sample=${file} && echo $n $sample && bedtools genomecov -g ' + genome + ' -i $file -bg -5 -strand $str > ${sample}_${n}.bg; done; done', shell=True)

#Function to generate full BedGraph files that we want, There are Triple Strings to deliminate file 
subprocess.check_call("""f_str="fw"; r_str="rev"; ext=".bg"; for file1 in *${f_str}${ext}; do file2=${file1/${f_str}/${r_str}} && outfile=${file1/${f_str}${ext}/fw_rev.bedgraph} && echo $file1 "+" $file2 "=" $outfile && awk 'BEGIN{OFS="\t"}{print $1,$2,$3,"-"$4}' $file2 | cat $file1 - | sort -k1,1 -k2,2n > $outfile; done""", shell=True)

#awk command to only get chromosomes that appear on the genome file
subprocess.check_call("for file in *.bedgraph; do echo $file && awk '$1 ~ /chr/' $file > ${file/.bedgraph/_chr.bedgraph}; done", shell=True)

#Sorts the bedgraph files to ensure bedGraphToBigWig works correctly
subprocess.check_call("for file in *chr.bedgraph; do echo $file && LC_COLLATE=C sort -k1,1 -k2,2n -k3,3n -s  $file > ${file/.bedgraph/_sorted.bedgraph}; done", shell=True)

#merge files so they can be converted to bigwig (There can't be overlap)
subprocess.check_call("for file in *sorted.bedgraph; do echo $file && bedtools merge -i $file -c 4 -d 0 -o max > ${file/sorted.bedgraph/merged.bedgraph}; done", shell=True)

#Sorts the bedgraph files to ensure bedGraphToBigWig works correctly
subprocess.check_call("for file in *merged.bedgraph; do echo $file && LC_COLLATE=C sort -k1,1 -k2,2n -k3,3n -s  $file > ${file/.bedgraph/_sorted2.bedgraph}; done", shell=True)

#Conversion to BigWIg
subprocess.check_call("for file in *sorted2.bedgraph; do echo $file && bedGraphToBigWig $file " + genome + " $file.bw; done", shell=True)


#Returns to the original working directory
os.chdir(wd)











