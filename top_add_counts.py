#!/usr/bin/python
################################################################################
#
# Count POPC, SOL, NA, and CL molecules in the not_protein.gro file
# Makes a backup topol.top_backup1 file.
#
# by Richard in 2017 for Python 2.7 MDTraj 1.8.0
#
# Changelog ([Date]):
#
################################################################################

# Packages
import os
from argparse import ArgumentParser
from shutil import copyfile

import mdtraj as md

def main(gro, topfile):

    u = md.load(gro)
    dir_path = os.path.dirname(os.path.realpath(topfile))

    add_tail = \
    ['POPC' + ' ' + str(len(u.topology.select('resname POPC and name P8'))) +'\n',
    'SOL' + ' ' + str(len(u.topology.select('water and name O'))) +'\n',
    'NA+' + ' ' + str(len(u.topology.select('name NA'))) +'\n',
    'CL-' + ' '+ str(len(u.topology.select('name CL'))) +'\n']

    # Make Backup of The Top File
    copyfile(topfile, topfile+'_backup1') # same directory as topfile

    # Open The File and Append The Result of the Counts
    f = open(topfile, 'r')
    lines = f.readlines()
    for t in add_tail:
        with open(topfile, 'a') as opf:
            opf.write(t)

if __name__ == '__main__':
    parser = ArgumentParser(
    description='Count the molecules in the system (POPC, SOL, NA, CL)')

    # Here we add all our arguments, each of these will be accessible as the
    # variable args.dest in this function. When something isn't required
    # make sure to add a default value for it.
    parser.add_argument(
    '-s', dest='grofile', type=str, required=True,
    help='a gro file generated from GROMACS')
    parser.add_argument(
    '-t', dest='topfile', type=str, required=True,
    help='top file from pdb2gmx')

    args = parser.parse_args()

    main(args.grofile, args.topfile)

    print 'Done adding molecule counts to the end of .top file.'
