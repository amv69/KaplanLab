#!/bin/bash
#
#SBATCH --job-name=NET_SEQ
#SBATCH -n 1
#SBATCH -t 1-00:00

source /ihome/ckaplan/amv69/.bashrc
source activate /ihome/ckaplan/amv69/miniconda3/envs/rnaseq

for f1 in *.fastq;
do
  echo $f1;
  fname=$(basename $f1);
  fastx_reverse_complement -i $f1 -o ${fname/.fastq/_RC.fastq};
done

module load umi-tools

for f1 in *R1*RC.fastq;
do
  echo $f1;
  f2=${f1/R1/R2};
  umi_tools extract --3prime \
    --stdin=$f1 --read2-in=$f2 \
    --bc-pattern=NNNN --bc-pattern2=NNNN \
    --stdout=${f1/RC/UMI} --read2-out=${f2/RC/UMI};
done

module purge

for f1 in *R1*UMI.fastq;
do
  echo $f1;
  f2=${f1/R1/R2};
  cutadapt -m 1 --overlap 7 \
    -g  CTTGGCACCCGAGAATTCCAN{4} \
    -G AGTTCTACAGTCCGACGATCN{4} \
    -o ${f1/UMI/Cut} -p ${f2/UMI/Cut} $f1 $f2;
done

for f1 in *R1*Cut.fastq;
do
  echo $f1;
  hisat2 -q --phred33 \
   --max-intronlen 4000 \
   --known-splicesite-infile \
   --no-unal /bgfs/ckaplan/Anand_seq/Genomes/INDEX_HISAT2/spo_sce_index/spo_sce_splicesites.txt \
   -x /bgfs/ckaplan/Anand_seq/Genomes/INDEX_HISAT2/spo_sce_index/ht2_spo_sce_index \
   -1 $f1 -2 ${f1/R1/R2} \
   -S ${f1/_Cut.fastq/.sam} \
   --rna-strandness RF \
   --secondary --no-mixed \
   --summary-file ${f1/_Cut.fastq/.txt};
done

for f1 in *.sam;
do
  echo $f1;
  samtools view -Sb $f1 -o ${f1/sam/bam};
done

#Generate Headers fpr the BAM files and out put as X_header.sam
for file in *bam;
do
        echo $file && samtools view -H ${file} > ${file/.bam/_header.sam};
done

#Generate file of unique
for f1 in *bam;
do
        f2=${f1/.bam/_header.sam} && echo $f1 $f2 && samtools view ${f1} | grep -w "NH:i:1" | cat ${f2} - | samtools view -Sb -
> ${f1/.bam/_unique.bam};
done

#sort unique reads
for file in *unique.bam;
do
        echo $file && samtools sort $file -o ${file/.bam/_sorted.bam} && rm $file;                                              
done
