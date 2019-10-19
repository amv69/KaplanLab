#!/bin/bash
#
#SBATCH --job-name=SNP
#SBATCH -n 1
#SBATCH -t 1:00:00
source /ihome/ckaplan/amv69/.bashrc
source activate /ihome/ckaplan/amv69/miniconda3/envs/rnaseq

#Cutadapt call for all R1 & R2 in current directory
for f1 in *R1.fastq;
do
	f2=${f1/R1/R2};
	echo $f1 $f2;
	cutadapt -g XT{50} -A A{50}X -O 5 \
	-o ${f1/.fastq/_cutadapt.fastq} \
	-p ${f2/.fastq/_cutadapt.fastq} ${f1} ${f2} \
	> ${f1/.fastq/cutadapt.txt};
done

for f1 in *R1_cutadapt.fastq;
do
	f2=${f1/R1/R2};
	echo $f1 $f2;
	hisat2 -q --dta --phred33 --max-intronlen 4000 \
	--known-splicesite-infile --no-unal \
	/bgfs/ckaplan/Anand_seq/Genomes/INDEX_HISAT2/spo_sce_index/spo_sce_splicesites_chr.txt \
	--rna-strandness RF --secondary --no-mixed \
	--summary-file ${f1/R1_cutadapt.fastq/hs2.txt} \
	-x /bgfs/ckaplan/Anand_seq/Genomes/INDEX_HISAT2/spo_sce_index/ht2_spo_sce_index \
	-1 ${f1} -2 ${f2} -S ${f1/R1_cutadapt.fastq/hs2.sam};
done

for file in *hs2.sam;
do
	echo $file;
	samtools view -b ${file} > ${file/sam/bam};
done

for f1

for file in *bam;
do
	echo $file && samtools view -H ${file} > ${file/.bam/_header.sam};
done

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
