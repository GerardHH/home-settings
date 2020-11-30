#!/usr/bin/python3

import argparse
import supervision
import env
from os import chdir, system
from typing import List


def __job(**other):
    ''' Start JOB service. '''
    job = 'JOB'
    chdir('{}/{}'.format(env.DESKTOP_CRUIZERPRO, job))
    prog = './{} --mgt ipc:///tmp/cpro/mgt/job.ipc --log ipc:///tmp/cpro/log.ipc --name job'.format(job)
    system(prog)


def __line_generator(**other):
    ''' Start line_generator service. '''
    line_generator = 'line_generator'
    chdir('{}/{}'.format(env.DESKTOP_CRUIZERPRO, line_generator))
    prog = './{} --mgt ipc:///tmp/cpro/mgt/line-generator.ipc --log ipc:///tmp/cpro/log.ipc --name line-generator'.format(line_generator)
    system(prog)


def __operation_planning(**other):
    ''' Start operation_planning_service. '''
    op = 'operation_planning_service'
    chdir('{}/{}'.format(env.DESKTOP_CRUIZERPRO, op))
    prog = './{} --mgt ipc:///tmp/cpro/mgt/operation_planning_service.ipc --log ipc:///tmp/cpro/log.ipc --name operation_planning_service'.format(op)
    system(prog)


def __no_service_selected(**other):
    ''' Print error. '''
    print('No service selected, please refer to ./start_service.py --help for more information')


def __system(cruizerpro: bool = False, disable: List[str] = None, enable: List[str] = None, **other):
    ''' Start the whole system in linux mode. Use the Booleans to overwrite the mode. '''
    mode = 'CRUIZERPRO' if cruizerpro else 'linux'
    if enable:
        supervision.__enable(services=enable)
    if disable:
        supervision.__disable(services=disable)
    chdir(env.DESKTOP_CRUIZERPRO)
    system('./system.sh {} --demo'.format(mode))


def __tango(gammaray: bool = False, **other):
    ''' Start tango service. Currently only CR12 is supported. '''
    chdir('{}/tango'.format(env.DESKTOP_CRUIZERPRO))
    prog = '{}./tango --mgt ipc:///tmp/cpro/mgt/tango-CR12.ipc --log ipc:///tmp/cpro/log.ipc --name tango'.format('gammaray ' if gammaray else '')
    system(prog)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start a service')
    parser.set_defaults(func=__no_service_selected)

    subparsers = parser.add_subparsers(title='Service', description='Which service to start')

    parser_job = subparsers.add_parser('job', help='Start the JOB service')
    parser_job.set_defaults(func=__job)

    parser_line_generator = subparsers.add_parser('line-generator', help='Start the line_generator service')
    parser_line_generator.set_defaults(func=__line_generator)

    parser_operation_planning = subparsers.add_parser('operation-planning', help='Start operation_planning_service')
    parser_operation_planning.set_defaults(func=__operation_planning)

    parser_system = subparsers.add_parser('system', help='Start the whole system, start the system in linux mode by default')
    parser_system.add_argument('-d', '--disable', nargs='+', type=supervision.__check_known_service, help='Disable services before starting the system, provide multiple services as a point seperated list')
    parser_system.add_argument('-e', '--enable', nargs='+', type=supervision.__check_known_service, help='Enable services before starting the system, provide multiple services as a point seperated list')
    parser_system_exclusive = parser_system.add_mutually_exclusive_group()
    parser_system_exclusive.add_argument('-c', '--cruizerpro', action='store_true', help='Start the system in CR7 mode')
    parser_system.set_defaults(func=__system)

    parser_tango = subparsers.add_parser('tango', help='Start the tango service for CR12')
    parser_tango.add_argument('-g', '--gammaray', action='store_true', help='Start tango with gammaray')
    parser_tango.set_defaults(func=__tango)

    args = parser.parse_args()
    args.func(**args.__dict__)
