#!/usr/bin/python3

import env
from os import chdir, system

chdir(env.DESKTOP_CRUIZERPRO)
system('./system.sh linux --demo')
