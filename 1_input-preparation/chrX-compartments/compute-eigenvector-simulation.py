import sys

import numpy as np

filename = sys.argv[1]
option = int(sys.argv[2])


def normalize(matrix):
    normalizing_matrix = np.zeros(shape=matrix.shape)

    for i in range(matrix.shape[0]):
        average_contact_probability = np.nanmean(
            np.diagonal(matrix, offset=i)
        )
        normalizing_matrix += np.diag(
            average_contact_probability
            * np.ones_like(np.diagonal(matrix, offset=i)),
            k=i,
        )
        normalizing_matrix += np.diag(
            average_contact_probability
            * np.ones_like(np.diagonal(matrix, offset=i)),
            k=-i,
        )

    return matrix / normalizing_matrix


contact_probability = np.loadtxt(filename)
normalized_matrix = normalize(contact_probability)

correlation_matrix = np.corrcoef(normalized_matrix)

_, eigenvectors = np.linalg.eig(correlation_matrix)
eigenvector = eigenvectors[:, 0]

np.savetxt(f"chrX-simulation.opt{option}.eigenvector", eigenvector)
