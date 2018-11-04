import casingSimulations
import dask
# import subprocess

# subprocess.Popen(['mpirun', '--np', '4', 'dask-mpi'], stdin=subprocess.DEVNULL)

# models to run
model_names = [
    "casing",
    "background",
    "permeable",
    "approx_casing",
    "approx_permeable",
    "approx_permeable2"
]

# Set up the simulation
@dask.delayed
def run_simulation(m):
    sim = casingSimulations.run.SimulationTDEM(
        modelParameters= m + ".json",
        meshGenerator='MeshParameters.json',
        srcList='sources.json',
        fields_filename=m + "_fields.npy"
    )
    fields = sim.run(verbose=True)
    return fields[:, '{}Solution'.format(sim.formulation), :]

f = {}
for m in model_names:
    f[m] = run_simulation(m)

dask.compute(f, num_workers=3) #, scheduler='distributed')


# # run the simulation
# fields = sim.run(verbose=True)

