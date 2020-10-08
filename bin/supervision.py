#!/usr/bin/python3

from os import system
from typing import List
import argparse
import env
import jsontools


def __check_known_service(service: str) -> str:
    ''' Check if service is a supported service. '''
    try:
        return env.SERVICES[service.lower()]
    except:
        raise argparse.ArgumentTypeError('Unknown service, supported services are: {}'.format(env.SERVICES))


def __disable(services: List[str], all: bool = False, **other):
    ''' Disable supervision for services. '''
    if not services and not all:
        raise RuntimeError('disable: No services and no --all, do not know what to do')
    for service in services if not all else env.SERVICES.values():
        __supervision(service=service, enable=False)


def __enable(services: List[str], all: bool = False, **other):
    ''' Enable supervision for services. '''
    if not services and not all:
        raise RuntimeError('enable: No services and no --all, do not know what to do')
    for service in services if not all else env.SERVICES.values():
        __supervision(service=service, enable=True)


def __list_of_services(services: str) -> List[str]:
    ''' Create a list of supported services based on services string. '''
    services_list = services.split('.')
    result = []
    for service in services_list:
        result.append(__check_known_service(service))
    return result


def __no_mode_selected(**other):
    ''' Print error for no mode. '''
    print('No mode selected, please refer to "supervision.py --help" for more information')


def __supervision(service: str, enable: bool, platform: str = 'linux'):
    ''' Enable/disable supervision for service in platform. '''
    query = ['services', service]
    add = {'startup': enable, 'restart': enable}
    jsontools.json_tools(file='{}/data/config/platforms/{}.json'.format(env.DESKTOP_CRUIZERPRO, platform), add=add, query=query, write=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Disable supervision for given service')
    parser.set_defaults(func=__no_mode_selected)

    subparsers = parser.add_subparsers(title='Mode')

    parser_enable = subparsers.add_parser('enable', help='Enable supervision, one of the options is required')
    parser_enable_service = parser_enable.add_mutually_exclusive_group()
    parser_enable_service.add_argument('-s', '--services', type=__list_of_services, help='Services to enable, provide point seperated list for multiple services')
    parser_enable_service.add_argument('-a', '--all', action='store_true', help='Enable supervision of all supported services')
    parser_enable.set_defaults(func=__enable)

    parser_disable= subparsers.add_parser('disable', help='Disable supervision, one of the options is required')
    parser_disable_service = parser_disable.add_mutually_exclusive_group()
    parser_disable_service.add_argument('-s', '--services', type=__list_of_services, help='Services to disable, provide point seperated list for multiple services')
    parser_disable_service.add_argument('-a', '--all', action='store_true', help='Disable supervision of all supported services')
    parser_disable.set_defaults(func=__disable)

    args = parser.parse_args()
    args.func(**args.__dict__)
