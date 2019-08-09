#!/bin/bash
#
#SBATCH --job-name=cut_and_align
#SBATCH -n 1
#SBATCH -t 2-00:00


module load umi-tools/0.5.5

for f1 in /bgfs/ckaplan/Anand_seq/NET_seq/Hiseq/18314Kap_N19007/*R1_001.fastq;
do
    filename=$(basename $f1) &&
    f2=${f1/R1/R2} &&
    filename2=$(basename $f2)
    echo $f1 $f2 &&
    umi_tools extract --stdin=${f1} --read2-in=${f2} --bc-pattern=NNNN --bc-pattern2=NNNN --stdout=${filename/.fastq/_UMI.fastq} --read2-out=${filename2/.fastq/_UMI.fastq};
done

module load cutadapt/1.18

for f1 in /bgfs/ckaplan/Anand_seq/NET_seq/Hiseq/18314Kap_N19007/*R2_001.fastq;
do
        filename=$(basename $f1) &&
        echo $f1 && cutadapt -a GATCGTCGGACTGTAGAACTCTGAAC -O 5 -o ${filename/.fastq/_cutadapt.fastq} ${f1} > cutadapt.txt;
done &&

module load hisat2/2.1.0

for f1 in *cutadapt.fastq;
do
        #TODO-FIX
        #Change it to match align3 output
        echo $f1 && hisat2 -q --phred33 --max-intronlen 4000 --known-splicesite-infile --no-unal /bgfs/ckaplan/Anand_seq/Genomes/INDEX_HISAT2/sce_index_2019/R64-1-1_chr_splicesites.txt -x /bgfs/ckaplan/Anand_seq/Genomes/INDEX_HISAT2/sce_index_2019/ht2_Budding_Fission ${f1} -S ${f1/UMI_cutadapt.fastq/hs2.sam} --rna-strandness R --secondary --no-mixed --summary-file ${f1/UMI_cutadapt.fastq/hs2.txt} &&
        hisat2 -q --phred33 --max-intronlen 4000 --known-splicesite-infile --no-unal /bgfs/ckaplan/Anand_seq/Genomes/INDEX_HISAT2/spo_index_2019/spo_chr_splicesites.txt  -x /bgfs/ckaplan/Anand_seq/Genomes/INDEX_HISAT2/spo_index_2019/ht2_Budding_Fission_spo ${f1} -S ${f1/UMI_cutadapt.fastq/hs2.sam} --rna-strandness R --secondary --no-mixed --summary-file ${f1/UMI_cutadapt.fastq/hs2.txt};
done &&

module load gcc/8.2.0
module load samtools/1.9

for f1 in *hs2.sam;
do
        echo $file && samtools sort $f1 > ${file/.sam/_sorted.sam};
done &&


module load deeptools/3.3.0

for f1 in *sorted.sam;
do
        echo $f1 && samtools index $f1 &&
	bamCoverage -b $f1 -o ${f1/_sorted.sam/.bw};
done
