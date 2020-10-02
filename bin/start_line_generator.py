#!/usr/bin/python3
from os import chdir, system
import env

line_generator = 'line_generator'
chdir('{}/{}'.format(env.DESKTOP_CRUIZERPRO, line_generator))
prog = './{} --mgt ipc:///tmp/cpro/mgt/line-generator.ipc --log ipc:///tmp/cpro/log.ipc --name line-generator'.format(line_generator)
system(prog)
