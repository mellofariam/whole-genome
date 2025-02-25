import sys
import math
import numpy as np
from OpenMiChroM.ChromDynamics import MiChroM

## Usage: collapse.py chr_number

replica_number = int(sys.argv[1])
chr_number = int(sys.argv[2])

sim = MiChroM(
    name=f"chr{chr_number}", temperature=2.0, time_step=0.01
)
sim.setup(
    platform="OpenCL", integrator="Langevin", precision="single"
)
sim.saveFolder(f"{replica_number}")
initStructure = sim.createSpringSpiral(
    ChromSeq=f"../2_inputs/chr{chr_number}_beads.txt",
    isRing=False,
)

# Loading the initial structure into sim object
sim.loadStructure(initStructure, center=True)

## Adding forces

# Bonded Potentials
sim.addFENEBonds(kfb=30.0)
sim.addAngles(ka=2.0)
sim.addRepulsiveSoftCore(Ecut=4.0)

# non Bonded Potentials
sim.addTypetoType(mu=3.22, rc=1.78)
sim.addIdealChromosome(mu=3.22, rc=1.78, dinit=3, dend=500)

# Collapse Potential
sim.addFlatBottomHarmonic(kr=5 * 10**-3, n_rad=10.0)

# Loops
sim.addLoops(
    mu=3.22,
    rc=1.78,
    X=-1.61299,
    looplists=[f"../2_inputs/chr{chr_number}_loops.txt"],
)

## Running the simulation to generate a collapsed structure
for _ in range(100):
    sim.runSimBlock(1000, increment=False)

## Running the annealing to return to Temperature = 1.0
for T in np.arange(2, 0.95, -0.05):
    sim.integrator.setTemperature(T / 0.00831446261815)
    for _ in range(40):
        sim.runSimBlock(1000, increment=False)

## Starting production simulation
sim.initStorage(filename=f"chr{chr_number}")

Rg = []
for frame in range(5000):
    sim.runSimBlock(1000, increment=True)
    sim.saveStructure()
    Rg.append(sim.chromRG())

    if frame > 500:
        average_Rg_values = np.mean(Rg[-100:])

        if math.isclose(Rg[-1], average_Rg_values, rel_tol=0.01):
            break

sim.saveStructure(mode="pdb")

sim.storage[0].close()
del sim

np.savetxt(f"Rg-chr{chr_number}.dat", Rg)
