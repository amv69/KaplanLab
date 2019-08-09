#!/bin/bash
#
#SBATCH --job-name=cut_and_align
#SBATCH -n 1
#SBATCH -t 1-00:00

module load deeptool/3.3.0

for f1 in *.bw;
do
  echo $f1 &&
  computeMatrix scale-regions --regionsFileName Dm.genes.indChromLabeled.bed \
  --scoreFileName $f1 --beforeRegionStartLength 200 --afterRegionStartLength 1000 \
  --regionBodyLength 1500 --binSize 10 \
  --outFileName ${f1/.bw/_matrix_scaledGenes} --sortRegions descend;
done

for f1 in *matrix_scaledGenes;
do
  echo $f1 &&
  plotHeatmap --matrixFile $f1 \
  --kmeans 2 \
  --sortUsing region_length \
  --outFileName ${f1/_matrix_scaledGenes/_two_clusters.pdf} \
  --plotTitle "Pol II" --whatToShow "heatmap and colorbar";
done
