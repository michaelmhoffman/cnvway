from gmtk.input_master import Covar, DPMF, DenseCPT, DiagGaussianMC, InputMaster, MX, Mean, NameCollection
from segway import run

input_master = InputMaster()

# set of labels
input_master.name_collection["emission"] = NameCollection("deletion", "neutral", "gain")

# mean parameter for each label
input_master.mean["deletion"] = Mean(-0.4)
input_master.mean["neutral"] = Mean(-0.14)
input_master.mean["gain"] = Mean(-0.11)
num_labels = len(input_master.mean)

# single covariance parameter tied across all labels
input_master.covar["tied"] = Covar(0.1)

# each label’s emission is a single-component mixture of Gaussians
input_master.dpmf["uniform"] = DPMF.uniform_from_shape(1)

for label in input_master.mean:
    input_master.mc[label] = DiagGaussianMC(mean=label, covar="tied")
    input_master.mx[label] = MX("uniform", label)

#transition model
input_master.dense_cpt["start"] = DenseCPT.uniform_from_shape(3)
input_master.dense_cpt["transition"] = DenseCPT.uniform_from_shape(3, 3, self=0.5)

input_master.save("input.master") 

run.main(["train-init", f"--num-labels={num_labels}", "--resolution=30000", "--distribution=norm", "--include-coords=include_coords.bed", 
"--input-master=input.master", "--structure=segway.str", "input.genomedata", "segway_output/traindir"])

run.main(["annotate", "--include-coords=include_coords.bed", "input.genomedata", "segway_output/traindir", "segway_output/annotatedir"])