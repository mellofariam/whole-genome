import sys
import numpy as np
from OpenMiChroM.ChromDynamics import MiChroM

replica = int(sys.argv[1])

nucleus = MiChroM(name="nucleus", temperature=1.5, time_step=0.01)
nucleus.setup(
    platform="OpenCL", integrator="Langevin", precision="single"
)

# Output folder:
nucleus.saveFolder(f"{replica}")

# Loading individual chromosomes:
chromosomes = nucleus.initStructure(
    mode="pdb",
    CoordFiles=[
        f"../3_collapse/{replica}/chr{chr_number}_collapsed.pdb"
        for chr_number in range(1, 47)
    ],
)

# Distributing individual chromosomes in the nucleus using the Fibonacci Sphere algorithm
chromosomes = nucleus.setFibPosition(chromosomes, factor=2.0)

# Loading chromosomes in the simulation context
nucleus.loadStructure(chromosomes, center=True)

# Saving the initial structure of the nucleus for visualization purpose
nucleus.saveStructure(mode="pdb")

# Homopolymer Potentials
nucleus.addFENEBonds(kfb=30.0)
nucleus.addAngles(ka=2.0)
nucleus.addRepulsiveSoftCore(Ecut=4.0)

# Collapse Potential
nucleus.addFlatBottomHarmonic(n_rad=0.8 * 53.36)

# Chromosome Potentials
nucleus.addTypetoType(mu=3.22, rc=1.78)

nucleus.addLoops(
    mu=3.22,
    rc=1.78,
    X=-1.612990,
    looplists=[
        f"../2_inputs/chr{chr_number}_loops.txt"
        for chr_number in range(1, 47)
    ],
)

# Ideal Chromosome Potential
for i in range(46):
    nucleus.addMultiChainIC(
        chainIndex=i, mu=3.22, rc=1.78, dinit=3, dend=500
    )

print("Simulation set... Starting calculations")
## Running the simulation to generate a collapsed structure @ T = 1.5

Rg = []
for _ in range(2000):
    nucleus.runSimBlock(1000, increment=False)
    Rg.append(nucleus.chromRG())


## Running the annealing to return to T = 1.0
for T in np.linspace(1.475, 1.0, num=20):
    nucleus.integrator.setTemperature(T / 0.00831446261815)
    nucleus.context.setParameter("kfb", 30)

    for _ in range(100):
        nucleus.runSimBlock(1000, increment=False)
        Rg.append(nucleus.chromRG())


print("Forces after annealing:")
nucleus.printForces()

## Including Nucleus Wall and removing Flat Bottom Harmonic Potential

nucleus.removeFlatBottomHarmonic()  # Removing Flat-Bottom Potential
nucleus.addAdditionalForce(nucleus.addSphericalConfinementLJ, r=53.36)

print("Flat Bottom Harmonic removed and Spherical Confinement added!")

## Equilibrating the system to the new added force

for _ in range(1000):
    nucleus.runSimBlock(1000, increment=False)
    Rg.append(nucleus.chromRG())

print("Forces after equilibration:")
nucleus.printForces()

## Starting sampling part of the simulation

nucleus.saveStructure(mode="pdb")

# Initiating .cndb file
nucleus.initStorage("nucleus", mode="w")

for frame in range(50_000):
    nucleus.runSimBlock(1000, increment=True)
    Rg.append(nucleus.chromRG())

    if frame % 100 == 0:
        nucleus.saveStructure()


print("Forces in the end:")
nucleus.printForces()

print("Simulation ended. Closing files...")

for i in range(46):
    nucleus.storage[i].close()

nucleus.saveStructure(mode="pdb")

np.savetxt(f"{replica}/radius-of-gyration.dat", Rg)

print("Files closed! All set!")
