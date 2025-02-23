# 1st Option: A -> positive and B -> negative

with open("chrX.eigenvector", "r") as eigenvector:
    with open("chr23_beads.opt1.txt", "w") as chrX_beads:
        for num, line in enumerate(eigenvector):
            if float(line) > 0:
                chrX_beads.write("{:} A1\n".format(num + 1))
            elif float(line) < 0:
                chrX_beads.write("{:} B1\n".format(num + 1))
            else:
                chrX_beads.write("{:} NA\n".format(num + 1))

# 2nd Option: A -> negative and B -> positive

with open("chrX.eigenvector", "r") as eigenvector:
    with open("chr23_beads.opt2.txt", "w") as chrX_beads:
        for num, line in enumerate(eigenvector):
            if float(line) > 0:
                chrX_beads.write("{:} B1\n".format(num + 1))
            elif float(line) < 0:
                chrX_beads.write("{:} A1\n".format(num + 1))
            else:
                chrX_beads.write("{:} NA\n".format(num + 1))
