#!/bin/bash
#
#SBATCH --job-name=cut_and_align
#SBATCH -n 1
#SBATCH -t 1-00:00

source /ihome/ckaplan/amv69/.bashrc
source activate /ihome/ckaplan/amv69/miniconda3/envs/rnaseq

for f1 in /bgfs/ckaplan/Alex/Introns/3p/*.bed;
do
  echo $f1;
  for f2 in ../data/*sorted.bam;
  do
      echo $f2;
      fname=$(basename $f1);
      fname2=$(basename $f2);
      filename1=${fname2/_sorted.bam/_};
      filename2=${fname/.bed/.bam};
      filename3="$filename1$filename2";
      echo $filename3;
      bedtools intersect -abam $f2 -b $f1 > $filename3;
  done
done

for f1 in *.bam;
do
        echo $f1 &&
        bamCoverage -b $f1 -o ${f1/.bam/.bw};
done
