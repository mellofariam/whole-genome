#!/bin/bash

# Iterate through all folders in the ../3_collapse directory
for folder in ../3_collapse/*; do
    if [ -d "$folder" ]; then
        for chr in {1..46}; do
            # Check if the file exists
            files=$(find "$folder" -name "chr${chr}_*.pdb")
            if [ -n "$files" ]; then
                for file in $files; do
                    mv "$file" "$folder/chr${chr}_collapsed.pdb"
                done
            fi
        done
    fi
done
