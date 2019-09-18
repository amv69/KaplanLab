#!/bin/bash
#
#SBATCH --job-name=cut_and_align
#SBATCH -n 1
#SBATCH -t 1-00:00

module load deeptools/3.3.0

for f1 in *.bw;
do
  echo $f1 &&
  computeMatrix reference-point --referencePoint TSS --regionsFileName introns.bed \
  --scoreFileName $f1 --beforeRegionStartLength 200 --afterRegionStartLength 1000 \
  -o ${f1/.bw/matrix}--outFileName ${f1/.bw/_matrix.tab} --sortRegions keep;
done

for f1 in *matrix;
do
  echo $f1 &&
  plotHeatmap --matrixFile $f1 \
  --sortUsing region_length \
  --outFileName visualOutput/${f1/_matrix/_heatmap.pdf} \
  --plotTitle "NET_Seq";
done
