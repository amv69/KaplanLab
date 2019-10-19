#!/bin/bash
#
#SBATCH --job-name=compare.py
#SBATCH -n 1
#SBATCH -t 1-00:00
#SBATCH --array=1-28
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=amv69@pitt.edu

source /ihome/ckaplan/amv69/.bashrc
source activate /ihome/ckaplan/amv69/miniconda3/envs/rnaseq

cd ~/bbTest/library_1

getFile()
{
gawk -v id="$SLURM_ARRAY_TASK_ID" '$1 == id {print $2}' ~/Github/indexed_libs.txt
}
f1=$(getFile)
python3 ~/Github/compare3.py $f1 ../lib1_Single_Variants_v1.fasta;
