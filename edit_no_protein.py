#!/usr/bin/python
################################################################################
#
# Run this script after you mutate the protein at one resid.
# This script will modify the not_protein.gro file if necessary.
# E.g. If you mutate from a VAL to ASP, remove a negative charge.
# If you mutate from a ASP TO GLU, do nothing.
#
# by Richard in 2017 for Python 2.7 MDTraj 1.8.0
#
# Changelog ([Date]):
#
################################################################################

# Packages
import os
import sys
from argparse import ArgumentParser

from shutil import copyfile
import numpy as np
import mdtraj as md

# Same parameters required to run mutate_model.py
def main(pro, nopro, resnum, resname_mut, chain):
    # Remember to log results when running in shell script
    #sys.stdout = open(dir_path + '/mutate_model.log', 'w') # Output console outputs to log file

    # Save Original Resname
    u = md.load(pro)
    resname_original = str(u.topology.residue(int(resnum)-1))[:3]
    print resname_original + resnum + ' to ' + resname_mut

    # Mutate the Protein in the protein_only pro file, executes mutate_model.py
    #print "mutate_model.py", pro, resnum, resname_mut, chain
    #sys.argv = ["mutate_model.py", pro, resnum, resname_mut, chain] # Pre-Set Arguments for mutate_model.py
    #execfile("mutate_model.py") # run mutate_model.py from MODELLER

    # Rename The Output File to something generic
    #IN  = pro + '%s%s.pdb' % (resname_mut, resnum)
    #OUT = pro[:-4] + '_mut' + pro[-4:]
    #os.rename(IN, OUT)

    #####################################
    # EDIT THE NOT_PROTEIN GRO FILE ...
    #####################################
    # If Switch is 0, nothing will be removed
    switch_remove = 0

    # Modify switch based off input and output resname
    # If original_resname is positive, you need to remove a negative charge (assuming going to neutral)
    # If resname_mut is positive, you need to remove a positive charge (assuming going from neutral)
    # The net of the two lines above will result in: removing a/multiple NA or CL
    for i, res in enumerate([resname_original, resname_mut]):
        if res in ['ASP', 'GLU']:
            # remove negative charge from bulk
            switch_remove += (-2*(i+1) + 3) # resname_original (-) then +1, resname_mut (-) then -1
        if res in ['ARG', 'LYS', 'HIS']:
            # remove positive charge from bulk
            switch_remove += (2*(i+1) - 3) # resname_original (+) then -1, resname_mut (-) then +1
        print switch_remove
    _ion = 'NA' if switch_remove > 0 else 'CL' # Define Ion to Remove

    for i in range(abs(switch_remove)):
        # Load not_protein.gro to modify: if _mut ver exists, load that instead
        if os.path.isfile('mut_' + nopro):
            u = md.load('mut_' + nopro)
        else:
            u = md.load(nopro)
        # Remove The Ion from the not_protein.gro file
        if switch_remove:
            print "Removing #%s: %s" % (i, _ion)
            ion = u.topology.select('name %s' % _ion)
            ion_pos = u.xyz[:,ion,2][0]
            ion_sel = ion[np.where(ion_pos == np.max(ion_pos))[0]]
            print "Removed Ion with Z-position:" + str(ion_pos[np.where(ion_pos == np.max(ion_pos))])

            # Exclude ion_sel from all of the atom indices, slice the trajectory, and save
            atom_indices = u.topology.select('all')
            atom_indices = np.delete(atom_indices, ion_sel)
            u = u.atom_slice(atom_indices)
            u.save('mut_' + nopro)
        else:
            u.save('mut_' + nopro)

if __name__ == '__main__':
    parser = ArgumentParser(
    description='Edit not_protein.gro file if needed after mutating protein')

    # Here we add all our arguments, each of these will be accessible as the
    # variable args.dest in this function. When something isn't required
    # make sure to add a default value for it.
    parser.add_argument(
    '-p', dest='pro', type=str, required=True,
    help='a protein_only pdb file generated from GROMACS')
    parser.add_argument(
    '-n', dest='nopro', type=str, required=True,
    help='a not_protein gro file generated from GROMACS')
    parser.add_argument(
    '-resnum', dest='resnum', type=str, required=True,
    help='resid to mutate (1-index) E.g. 1 = MET')
    parser.add_argument(
    '-resname', dest='resname', type=str, required=True,
    help='3 upper case letter protein code to mutate to. E.g. THR, ARG, ASP')
    parser.add_argument(
    '-chain', dest='chain', type=str, required=False, default='A',
    help='chain of protein to mutate')

    args = parser.parse_args()

    main(args.pro, args.nopro, args.resnum, args.resname, args.chain)

    print 'Done Editing Not_Protein.gro File.'
