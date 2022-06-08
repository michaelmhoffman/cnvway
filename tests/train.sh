segway train-init \
--num-labels=3 \
--resolution=30000 \
--distribution=norm \
--include-coords=data/tumour-normal_merge_include_coords.bed \
--input-master=input.master \
--structure=segway.str \
data/train-data.genomedata cnvway_output/traindir