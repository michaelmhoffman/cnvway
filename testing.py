from GMTK_input_master import Covar, DPMF, DenseCPT, DiagGaussianMC, InputMaster, MX, Mean, NameCollection

traindir = "test3_output/traindir"
annotatedir = "test3_output/annotatedir"

input_master = InputMaster()

input_master.name_collection["emission"] = NameCollection("deletion", "neutral", "gain")

input_master.mean["deletion"] = Mean(-0.4)
input_master.mean["neutral"] = Mean(-0.14)
input_master.mean["gain"] = Mean(-0.11)

input_master.covar["tied"] = Covar(0.1)

input_master.dense_cpt["start"] = DenseCPT.uniform_from_shape(3)
input_master.dense_cpt["transition"] = DenseCPT.uniform_from_shape(3, 3, self=0.5)

input_master.dpmf["uniform"] = DPMF.uniform_from_shape(1)

for label in input_master.mean:
    input_master.mc[label] = DiagGaussianMC(mean=label, covar="tied")
    input_master.mx[label] = MX("uniform", label)

input_master.save("input.master", traindir) #default assumes path to traindir is 'segway_output/traindir'

from segway import run

run.main(["train-init", "--num-labels=3", "--resolution=30000", "--distribution=norm", "--include-coords=data/tumour-normal_merge_include_coords.bed", 
"--input-master=input.master", "--structure=segway.str", "data/train-data.genomedata", traindir])

run.main(["annotate", "--include-coords=data/tumour-normal_merge_include_coords.bed", "data/train-data.genomedata", traindir, annotatedir])