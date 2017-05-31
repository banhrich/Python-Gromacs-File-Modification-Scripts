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

def main(topfile, basefile):
    dir_path = os.path.dirname(os.path.realpath(topfile))

    copyfile(topfile, topfile+'_backup_2')
    f = open(topfile, 'r').readlines()

    # Top of File Details
    e = 0
    for line in f:
        if line.find(';') == -1: break
        e += 1
    intro = f[:e]

    # Body/Middle Section -> prot.itp
    b, e = 0, 0
    for line in f:
        if line.find('[ moleculetype ]') != -1: break
        b += 1

    for line in f[::-1]:
        e -= 1
        if line.find('Include Position restraint file') != -1: break
    for line in f[e:]:
        if line.find('#endif') != -1:
            break
        e += 1
    body = f[b:e+1]

    # Bottom Section -> topol.top
    e = 0
    for line in f[::-1]:
        e -= 1
        if line.find('[ molecules ]') != -1: break
    end = f[e:]

    # Forcefield Base File
    base = open(basefile, 'r').readlines();

    TOP = []; TOP.extend(intro); TOP.extend(base); TOP.extend(end)
    ITP = []; ITP.extend(intro); ITP.extend(body)

    with open(dir_path + '/topol.top', 'w') as opf:
        for line in TOP:
            opf.write(line)
    with open(dir_path + '/prot.itp', 'w') as opf:
        for line in ITP:
            opf.write(line)

if __name__ == '__main__':
    parser = ArgumentParser(
    description='Count the molecules in the system (POPC, SOL, NA, CL)')

    # Here we add all our arguments, each of these will be accessible as the
    # variable args.dest in this function. When something isn't required
    # make sure to add a default value for it.
    parser.add_argument(
    '-t', dest='topfile', type=str, required=True,
    help='.top file generated from pdb2gmx')
    parser.add_argument(
    '-b', dest='basefile', type=str, required=True,
    help='base top file containing forcefield parameters')

    args = parser.parse_args()

    main(args.topfile, args.basefile)

    print 'Done modifying .top file and generating prot.itp.'
