import sys
import numpy as np
from OpenMiChroM.ChromDynamics import MiChroM

replica = int(sys.argv[1])
option = int(sys.argv[2])

sim = MiChroM(name="chr23", temperature=2.0, time_step=0.01)
sim.setup(
    platform="OpenCL", integrator="Langevin", precision="single"
)
sim.saveFolder(f"option{option}")
initStructure = sim.createSpringSpiral(
    ChromSeq=f"chr23_beads.opt{option}.txt"
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
sim.addLoops(looplists=["../../2_inputs/chr23_loops.txt"])

## Running the simulation to generate a collapsed structure
for _ in range(100):
    sim.runSimBlock(1000, increment=False)

## Running the annealing to return to Temperature = 1.0
for T in np.arange(2, 0.95, -0.05):
    sim.integrator.setTemperature(T / 0.00831446261815)
    for _ in range(40):
        sim.runSimBlock(1000, increment=False)

## Starting production simulation
sim.initStorage(filename="chr23.opt{option}.{replica}")

for _ in range(5000):
    sim.runSimBlock(1000, increment=True)
    sim.saveStructure()

sim.storage[0].close()
del sim
