import numpy as np
import time
import h5py
import sys
from scipy.spatial import distance

"""
run with arguments 
$1 : .cndb files from different replicas to be read
"""

start = time.time()

files = sys.argv[1:]  # .cndb files from different replicas

mu = 3.22  # parameter for contact function f
r_cut = 1.78  # parameter for contact function f

print("Number of replicas to process: {:}".format(len(files)))

with h5py.File(files[0], "r") as replica1:
    chr_size = int(len(replica1["1"]))

contact_probability = np.zeros((chr_size, chr_size))

total_frames = 0
for filename in files:

    chro = h5py.File(filename, "r")  # comando para abrir o arquivo

    frames = len(chro.keys()) - 1

    print(
        "Processing file {:} with {:} frames...".format(
            filename, frames
        )
    )

    for i in range(1, frames + 1):
        positions = np.asarray(chro[str(i)])

        contact_probability += 0.5 * (
            1.0
            + np.tanh(
                mu
                * (
                    r_cut
                    - distance.cdist(
                        positions, positions, "euclidean"
                    )
                )
            )
        )

        total_frames += 1

    chro.close()
    end = time.time()
    elapsed = end - start

    print("Processed file {:} in %.3f s".format(filename) % elapsed)

np.savetxt(
    "chrX-contact-probability.dat",
    np.divide(contact_probability, total_frames),
)

end = time.time()
elapsed = end - start

print("Total number of frames: {:}".format(total_frames))
print("File saved: chrX-contact-probability.dat\n")
print("Ran in %.3f sec" % elapsed)
print("############################################################")
