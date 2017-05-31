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

def main(mdp, time):
    dir_path = os.path.dirname(os.path.realpath(mdp))
    f = open(mdp, 'r').readlines()

    # Find Time Step
    for line in f:
        if line.find('dt') != -1:
            dt = float(line[line.find('=')+2:line.find(';')])
            break
    steps = int(time * 10**2 / dt) # Total steps required for given time

    # Write new md.mdp file for production
    with open(dir_path + '/md.mdp', 'w') as opf:
        for line in f:
            if line.find('nsteps') != -1:
                b = line.find('=')
                e = line.find(';')
                line = line[:b+2] + str(steps) + line[e-1:]
            opf.write(line)

if __name__ == '__main__':
    parser = ArgumentParser(
    description='Modify base mdp file and generate new mdp file with given time (ns)')

    # Here we add all our arguments, each of these will be accessible as the
    # variable args.dest in this function. When something isn't required
    # make sure to add a default value for it.
    parser.add_argument(
    '-m', dest='mdpfile', type=str, required=True,
    help='a template / base mdp file')
    parser.add_argument(
    '-time', dest='time', type=int, required=True,
    help='Total Time for Simulation in ns. E.g. 200 will be 200ns')

    args = parser.parse_args()

    main(args.mdpfile, args.time)

    print 'Done generating mdp file.'
