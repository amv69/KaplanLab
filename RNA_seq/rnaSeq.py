

#Cutadapt call for all R1 & R2 in current directory
for f1 in *R1.fastq;
do
	f2=${f1/R1/R2} && echo $f1 $f2 && cutadapt -g XT{50} -A A{50}X -O 5 -o ${f1/.fastq/_cutadapt.fastq} -p ${f2/.fastq/_cutadapt.fastq} ${f1} ${f2} > ${f1/.fastq/cutadapt.txt};
done

for f1 in *R1_cutadapt.fastq;
do
	f2=${f1/R1/R2} && echo $f1 $f2 && hisat2 -q --phred33 --max-intronlen 4000 --known-splicesite-infile --no-unal /bgfs/ckaplan/Anand_seq/Genomes/INDEX_HISAT2/spo_sce_index/spo_sce_splicesites_chr.txt --rna-strandness RF --secondary --no-mixed --summary-file ${f1/R1_cutadapt.fastq/hs2.txt} -x /bgfs/ckaplan/Anand_seq/Genomes/INDEX_HISAT2/spo_sce_index/ht2_spo_sce_index -1 ${f1} -2 ${f2} -S ${f1/R1_cutadapt.fastq/hs2.sam};
done

#Call to convert SAM to BAM(-b) TO-DO: -S has been deprecated, make sure it works w/o
for file in *hs2.sam;
do
	echo $file && samtools view -S -b ${file} > ${file/sam/bam};
done

#Generate Headers fpr the BAM files and out put as X_header.sam
for file in *bam;
do
	echo $file && samtools view -H ${file} > ${file/.bam/_header.sam};
done

#Generate file of unique
for f1 in *bam;
do
	f2=${f1/.bam/_header.sam} && echo $f1 $f2 && samtools view ${f1} | grep -w "NH:i:1" | cat ${f2} - | samtools view -Sb - > ${f1/.bam/_unique.bam};
done

#sort unique reads
for file in *unique.bam;
do
	echo $file && samtools sort $file -o ${file/.bam/_sorted.bam} && rm $file;
done

#index
for file in *sorted.bam;
	do echo $file && samtools index -b $file;
done

for file in *sorted.bam;
do
	echo $file && samtools idxstats $file | cut -f 1 | grep -v chrM | xargs samtools view -b $file > ${file/.bam/_mt.bam};
done

for file in *mt.bam;
do
	echo $file && bedtools bamtobed -cigar -i $file > ${file/_unique_sorted_plus_mt.bam/.bed};
done

#Get genomecoverage for bed files
for str in "+" "-";
do
	[ "$str" = "+" ] && n="rev" || n="fw"; for file in *.bed;
	do
		sample=${file} && echo $n $sample && bedtools genomecov -g /bgfs/ckaplan/Anand_seq/Genomes/Combined_yeast/Budding_Fission_new.genome -i $file -bg -5 -strand $str > ${sample}_${n}.bg;
  done;
done

#Function to generate full BedGraph files that we want
f_str="fw";
r_str="rev";
ext=".bg";
for file1 in *${f_str}${ext};
do
	file2=${file1/${f_str}/${r_str}} && outfile=${file1/${f_str}${ext}/fw_rev.bedgraph} && echo $file1 "+" $file2 "=" $outfile && awk 'BEGIN{OFS="\t"}{print $1,$2,$3,"-"$4}' $file2 | cat $file1 - | sort -k1,1 -k2,2n > $outfile;
done

#awk command to only get chromosomes that appear on the genome file
for file in *.bedgraph;
do
	echo $file && awk '$1 ~ /chr/' $file > ${file/.bedgraph/_chr.bedgraph};
done

#Sorts the bedgraph files to ensure bedGraphToBigWig works correctly
for file in *chr.bedgraph;
do
	echo $file && LC_COLLATE=C sort -k1,1 -k2,2n -k3,3n -s  $file > ${file/.bedgraph/_sorted.bedgraph};
done

#merge files so they can be converted to bigwig (There can't be overlap)
subprocess.check_call("for file in *sorted.bedgraph; do echo $file && bedtools merge -i $file -c 4 -d 0 -o max > ${file/sorted.bedgraph/merged.bedgraph}; done", shell=True)

#Sorts the bedgraph files to ensure bedGraphToBigWig works correctly
subprocess.check_call("for file in *merged.bedgraph; do echo $file && LC_COLLATE=C sort -k1,1 -k2,2n -k3,3n -s  $file > ${file/.bedgraph/_sorted2.bedgraph}; done", shell=True)

#Conversion to BigWIg
subprocess.check_call("for file in *sorted2.bedgraph; do echo $file && bedGraphToBigWig $file /bgfs/ckaplan/Anand_seq/Genomes/Combined_yeast/Budding_Fission_new.genome $file.bw; done", shell=True)


#Returns to the original working directory
os.chdir(wd)
