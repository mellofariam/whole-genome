import shutil

subcmpt_file = open("GSE63525_GM12878_subcompartments.bed", "r")

resolution = 50000
chro_number = " "

for line in subcmpt_file:
    info = line.split()

    if info[0] != chro_number:
        if chro_number != " ":
            print("{:} {:}".format(chro_number, beads - 1))
            chro_file.close()
            shutil.copyfile(
                f"../../2_inputs/{chro_number}_beads.txt",
                f"../../2_inputs/chr{int(chro_number[3:])+23}_beads.txt",
            )

        chro_file = open(f"../../2_inputs/{info[0]}_beads.txt", "w+")
        beads = 1

    chro_number = info[0]

    frag_size = int((int(info[2]) - int(info[1])) / resolution)

    for i in range(frag_size):
        chro_file.write("{:} {:}\n".format(beads, info[3]))
        beads += 1

print("{:} {:}".format(chro_number, beads - 1))
chro_file.close()

shutil.copyfile(
    f"../../2_inputs/{chro_number}_beads.txt",
    f"../../2_inputs/chr{int(chro_number[3:])+23}_beads.txt",
)

subcmpt_file.close()
