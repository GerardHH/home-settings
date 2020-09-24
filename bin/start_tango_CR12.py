#!/usr/bin/python3

from os import chdir, system
import argparse
import env

parser = argparse.ArgumentParser(description='Start tango service')
parser.add_argument('-g', '--gammaray', action='store_true', help='Start tango with gammaray')
args = parser.parse_args()

chdir('{}/tango'.format(env.DESKTOP_CRUIZERPRO))
prog = '{}./tango --mgt ipc:///tmp/cpro/mgt/tango-CR12.ipc --log ipc:///tmp/cpro/log.ipc --name tango'.format('gammaray ' if args.gammaray else '')
system(prog)
