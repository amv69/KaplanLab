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

for f1 in *R2_*;
do
        filename=$(basename $f1) &&
        echo $f1 && cutadapt -a GATCGTCGGACTGTAGAACTCTGAAC -O 5 -o ${filename/.fastq/_cutadapt.fastq} ${f1} > cutadapt.txt;
done &&


module load hisat2/2.1.0

for f1 in *cutadapt.fastq;
do
        echo $f1 && hisat2 -q --phred33 --max-intronlen 4000 --known-splicesite-infile --no-unal /bgfs/ckaplan/Anand_seq/Genomes/INDEX_HISAT2/spo_sce_index/spo_sce_splicesites.txt -x /bgfs/ckaplan/Anand_seq/Genomes/INDEX_HISAT2/spo_sce_index/ht2_spo_sce_index -1 $f1 -2 ${f1/R1/R2} -S ${f1/UMI_cutadapt.fastq/_hs2.sam} --rna-strandness RF --secondary --no-mixed --summary-file ${f1/UMI_cutadapt.fastq/_hs2.txt} &&

done &&

module load gcc/8.2.0
module load samtools/1.9

for f1 in *hs2.sam;
do
        echo $file && samtools view -q 10 -Sbu $f1 | samtools sort > ${file/.sam/_uniq_sorted.bam};
done &&

for f1 in *sorted.bam;
do
        echo $f1 && samtools index $f1 && samtools idxstats $f1 > ${f1/.bam/_idxstats.txt};
done
