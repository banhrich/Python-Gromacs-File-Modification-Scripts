# File Descriptions

// mutate_model.py

MODELLER substitution script. Can be found here: https://salilab.org/modeller/wiki/Mutate%20model

## edit_not_protein.py

This will substract an ion from the system ( NA+ or CL- ) depending
on the mutation introduced. This factors in the original residue name
and mutation residue name to decide which ion and how many to remove.

## top_add_counts.py

This script will calculate the number of molecules POPC, SOL, NA+, CL-
in the gro file and append this information to the end of the top file.
Should supply the no_protein.gro and topol.top files to this script

## top_modify.py

Split the topol.top file into a topol.top and prot.itp file. This script
requires a basefile that contains the content that will go into the 
topol.top file. (i.e. forcefields). Original topol.top forcefield 
parameters will likely not be sufficient for the system. Replacing these
forcefields should help.

## pnp_merge.py

Merges protein_only.gro and not_protein.gro files. This step follows
after mutating protein_only.pdb, pdb2gmx AND modifying the not_protein.gro
file.









