import numpy as np

with open(
    "GSE63525_GM12878_primary+replicate_HiCCUPS_looplist.txt", "r"
) as loops_file:

    loops_list = {}
    resolution = 50000

    for num, line in enumerate(loops_file):
        info = line.split()
        if num > 0:
            if info[0] not in loops_list:
                loops_list.update({info[0]: []})

            anchor1 = np.mean([int(info[1]), int(info[2])])

            if anchor1 % resolution == 0:
                x = int(anchor1 // resolution)
            elif anchor1 % resolution != 0:
                x = int(anchor1 // resolution + 1)

            anchor2 = np.mean([int(info[4]), int(info[5])])

            if anchor2 % resolution == 0:
                y = int(anchor2 // resolution)
            elif anchor1 % resolution != 0:
                y = int(anchor2 // resolution + 1)

            if x != y and x != y + 1 and x != y - 1:
                loops_list[info[0]].append("{:} {:}".format(x, y))

    for key in loops_list:
        chromosome = int(key) if key != "X" else 23
        np.savetxt(
            f"../../2_inputs/chr{chromosome}_loops.txt",
            loops_list[key],
            fmt="%s",
        )

        # Save copy of loop list for the other homologous chromosome
        if chromosome != 23:
            np.savetxt(
                f"../../2_inputs/chr{chromosome+23}_loops.txt",
                loops_list[key],
                fmt="%s",
            )
