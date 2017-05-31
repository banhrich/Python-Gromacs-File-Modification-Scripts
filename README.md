This is a collection of scripts used to modify important and commonly used GROMACS files. The files modified are the ones from Gromacs v4.0.6.

# File Descriptions

## edit_not_protein.py

This will substract an ion from the system (set to NA+ or CL- ) depending
on the mutation introduced. This factors in the original residue name (queried via resID)
and mutation residue name (3-letter code) to decide which ion, if any, to remove. Modification of the ion type may be required for your system if you reuse this script. (Will update for general purposes in the future.)

## top_add_counts.py

This script will calculate the number of molecules POPC, SOL, NA+, CL- (these can be changed within the file)
in the gro file and append this information to the end of the top file. The order of the molecules should match the order of the 'final' GRO file.

Should supply the no_protein.gro and topol.top files to this script

## top_modify.py

Split the topol.top file into a topol.top and prot.itp file. This script
requires a base file (base.top) that contains the contents that will go into the 
topol.top file. (i.e. forcefields). Original topol.top forcefield 
parameters generated from pdb2gmx may not be sufficient. Replacing these
forcefields with the ones in base.top should help. This script is useful for automation purposes.

## pnp_merge.py

Merges protein_only.gro and not_protein.gro files. This can easily be done in line via Bash as well.
