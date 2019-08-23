#!/bin/bash
#
#SBATCH --job-name=cut_and_align
#SBATCH -n 1
#SBATCH -t 1-00:00

module load deeptools/3.3.0

for f1 in *.bw;
do
  echo $f1 &&
  computeMatrix reference-point -R introns.bed \
  -S $f1 --beforeRegionStartLength 500 --afterRegionStartLength 1000 \
  --outFileName ${f1/.bw/_matrix_scaledGenes} --sortRegions descend;
done

for f1 in *matrix_scaledGenes;
do
  echo $f1 &&
  plotHeatmap --matrixFile $f1 \
  --outFileName visualOutput/${f1/_matrix_scaledGenes/_two_clusters.pdf} \
  --plotTitle "Intron";
done
