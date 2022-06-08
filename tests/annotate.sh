srun -p hoffmangroup --ntasks=1 --nodes=1 --mem=32000  \
segway annotate \
--include-coords=data/tumour-normal_merge_include_coords.bed \
data/train-data.genomedata cnvway_output/traindir cnvway_output/annotatedir