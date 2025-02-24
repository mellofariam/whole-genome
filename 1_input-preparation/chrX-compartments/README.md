# Determining chrX compartment sequence

1. Extract eigenvector from Hi-C map (made with [JuicerTools 1.22.01](https://github.com/aidenlab/juicer/wiki/Download))

    ```
    java -Xmx32g -jar juicer_tools_1.22.01.jar eigenvector KR https://ftp.ncbi.nlm.nih.gov/geo/series/GSE63nnn/GSE63525/suppl/GSE63525%5FGM12878%5Finsitu%5Fprimary%2Breplicate%5Fcombined%2Ehic X BP 50000 chrX.eigenvector -p
    ```

2. Create two A/B sequences, one with the positive values in the eigenvector as A, and another with positive values as B.

3. Run simulations with each sequence, and then compare *in silico* eigenvector with experimental one to determine which sequence to use.

4. Move the appropriate sequence to `2_inputs`

    ```
    cp chr23_beads.opt1.txt ../../2_inputs/chr23_beads.txt 
    cp chr23_beads.opt1.txt ../../2_inputs/chr46_beads.txt 
    ```