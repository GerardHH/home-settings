#!/usr/bin/python3
import env
from os import chdir, system
op = 'operation_planning_service'

chdir('{}/{}'.format(env.DESKTOP_CRUIZERPRO, op))
prog = './{} --mgt ipc:///tmp/cpro/mgt/operation_planning_service.ipc --log ipc:///tmp/cpro/log.ipc --name operation_planning_service'.format(op)
system(prog)
