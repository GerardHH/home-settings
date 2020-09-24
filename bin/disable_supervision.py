#!/usr/bin/python3

import json_tools
import env

from os import system
import argparse

parser = argparse.ArgumentParser(description='Disable supervision for given service')
parser.add_argument('-e', '--enable', action='store_true', help='Enable supervision instead')
parser.add_argument('service', help='The service that will be disabled')
args = parser.parse_args()

query = 'services.{}'.format(args.service)
add = {'startup': args.enable, 'restart': args.enable}
json_tools.json_tools(file='{}/data/config/platforms/linux.json'.format(env.DESKTOP_CRUIZERPRO), add=add, query=query, write=True)
