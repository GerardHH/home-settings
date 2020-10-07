#!/usr/bin/python3
from os import chdir, system
import env

job = 'JOB'
chdir('{}/{}'.format(env.DESKTOP_CRUIZERPRO, job))
prog = './{} --mgt ipc:///tmp/cpro/mgt/job.ipc --log ipc:///tmp/cpro/log.ipc --name job'.format(job)
system(prog)
